"""
Generic handler functionality for Phantom App connector implementations.

To implement a basic connector that supports a hypothetical `echo message`
action and provides a result summary:
```
@main_connector
class MyConnector(HandlerMixin):
    @ActionHandler
    def echo_message(self, message, context=None):
        self.logger.info('message: %r', message)
        yield message

    @echo_message.summary
    def get_summary(self, results):
        message, = results
        return {'message': message}
```
"""
import asyncio
import json
import logging
from abc import ABCMeta
from functools import lru_cache, partial, update_wrapper, wraps
from inspect import isasyncgen
from logging.handlers import RotatingFileHandler
from pathlib import Path

import phantom.vault
from phantom.action_result import ActionResult
from phantom.app import APP_ERROR, APP_SUCCESS
from phantom.base_connector import BaseConnector


logger = logging.getLogger(__name__)


class ConnectorLogHandler(logging.Handler):
    """
    Delegates logging calls to app interface functions, and provides filthy
    hacks to write to a logging file
    """
    FIELDS = [
        '{levelname}',
        '{name}',
        '{message}',
    ]

    FIELD_SEPARATOR = ' : '

    FORMAT_STRING = f' {FIELD_SEPARATOR.join(FIELDS)}'

    FORMATTER = logging.Formatter(FORMAT_STRING, style='{')

    FILE_FORMATTER = logging.Formatter(
        f'[%(asctime)s] {logging.BASIC_FORMAT}', style='%')

    def __init__(self, connector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connector = connector
        self.setFormatter(self.FORMATTER)
        self._file_handler = None

    @property
    def file_handler(self):
        # This needs to be instantiated after after the connector;
        # Assuming any logging calls will occur after the state directory
        # is ready to use.
        if self._file_handler is not None:
            return self._file_handler

        logs_directory = self.connector.get_logs_path()
        logs_directory.mkdir(exist_ok=True)
        connector_log = logs_directory.joinpath('connector.log')
        self._file_handler = RotatingFileHandler(
            filename=connector_log, maxBytes=1024*1024, backupCount=5)
        self._file_handler.setFormatter(self.FILE_FORMATTER)
        return self._file_handler

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        if record.levelno >= logging.ERROR:
            self.connector.error_print(message)
        else:
            self.connector.debug_print(message)

        if record.levelno >= logging.INFO:
            self.connector.save_progress(record.message)

        self.file_handler.emit(record=record)


class ResultContext:
    """
    Manages the creation, status reporting, and error handling of an
    ActionResult.
    """
    def __init__(self, connector, param, context_data):
        self.connector = connector
        self.action_result = ActionResult(dict(param))
        self.context_data = context_data
        self._old_context = None

    def __enter__(self):
        self.action_result = self.connector.add_action_result(
            self.action_result)
        self._old_context = self.connector.context
        self.connector.context = self.context_data
        return self.action_result

    def __exit__(self, exc_type, exc_value, traceback):
        self.connector.context = self._old_context
        self._old_context = None
        if exc_type is None:
            self.action_result.set_status(APP_SUCCESS)
            return None

        # Phantom appears to expect errors to be handled by the connector.
        # Report and log the error, but suppress it from propagating.
        self.connector.logger.error(str(exc_value), exc_info=exc_value)
        self.action_result.set_status(
            APP_ERROR, exc_type.__name__, exception=exc_value)
        return True


class StateContext:
    def __init__(self, connector):
        self.connector = connector
        self._data = None

    @property
    def data(self):
        if self._data is None:
            try:
                with self.connector.open_state() as state_file:
                    self._data = json.load(state_file)

            except FileNotFoundError:
                self._data = {}

        return self._data

    def __enter__(self):
        self.connector.state_context = self

    def __exit__(self, *args, **kwargs):
        if self._data is not None:
            with self.connector.open_state(path=None, mode='w') as state_file:
                json.dump(self.connector.state, state_file)


class ActionHandler:
    registered_handlers = {}
    """
    A descriptor for a method designated as an action handler for a connector
    class.
    When used as a decorator, it provides a straightforward way to register
    the decorated method as an action handler.

    This class wraps the provided method with standard error handling, and
    manages the conversion of generic method results to Phantom ActionResults.

    :param function method: The method that implements the connector's action
        handler logic for the action of the same name
    """
    def __init__(
            self,
            method=None,
            *,
            data_contains=None,
            action_type=None,
            read_only=False,
    ):
        self.unbound_method = None
        self.handler_method = None
        self.summary_method_name = None
        self.data_contains_map = data_contains
        self.summary_contains_map = None
        self.action_type = action_type
        self.read_only = read_only
        if method is not None:
            self.decorate_method(method=method)

    def __call__(self, method):
        return self.decorate_method(method=method)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        bound_method = partial(self.unbound_method, instance)
        update_wrapper(bound_method, self.unbound_method)
        return bound_method

    @property
    def action_identifier(self):
        return self.unbound_method.__name__

    def decorate_method(self, method):
        self.unbound_method = method
        self.handler_method = self.create_handler_method()
        handler_set = self.registered_handlers.setdefault(
            self.action_identifier, set())

        handler_set.add(self)
        return self

    def create_handler_method(self):
        """
        Wrap the action handler logic in standard Phantom ActionResult results
        and error-handling

        :return: A new unbound method that wraps the original in Phantom
            reporting and error handling
        :rtype: function
        """
        action_identifier = self.action_identifier

        @wraps(self.unbound_method)
        def handler_method(connector, param):
            connector.logger.info('Handling %r', action_identifier)
            context = param.pop('context', None)
            with ResultContext(connector, param, context) as action_result:
                data_source = self.unbound_method(connector, **param)
                try:
                    data_iterable = iter(data_source)
                except TypeError:
                    connector.logger.debug('Data not iterable; assuming async')
                    self.consume_async_data(
                        connector, action_result, data_source)
                else:
                    for data in data_iterable:
                        connector.logger.debug(
                            'Adding %r result data', action_identifier)
                        action_result.add_data(data)

                if self.summary_method_name is None:
                    connector.logger.debug(
                        'No summary method for %r handler', action_identifier)
                else:
                    summary_method = getattr(
                        connector, self.summary_method_name)
                    results = action_result.get_data()
                    connector.logger.debug(
                        'Creating summary for %r', action_identifier)
                    summary = summary_method(results)
                    action_result.set_summary(summary)

                connector.logger.info(
                    'Finished handling %r', action_identifier)

            return action_result

        return handler_method

    def summary(self, unbound_method):
        """
        A decorator for a connector method that will produce a summary from
        the result of a call to a handler

        :param function unbound_method: The summary method
        :return: The summary method
        :rtype: function
        """
        self.summary_method_name = unbound_method.__name__
        return unbound_method

    def summary_contains(self, summary_contains_map):
        self.summary_contains_map = summary_contains_map
        return self.summary

    @classmethod
    def data_contains(cls, data_contains_map):
        logger.warning(
            'Use %s constructor parameters instead of %s.data_contains',
            cls,
            cls,
        )
        return cls(data_contains=data_contains_map)

    async def consume_async_generator(
            self, connector, action_result, generator):
        connector.logger.debug('Consuming from async generator %r', generator)
        data_queue = asyncio.Queue()
        async def enqueue_data():
            connector.logger.debug('Enqueuing data using %r', generator)
            async for data in generator:
                connector.logger.debug('Putting data %r', data)
                await data_queue.put(data)

        loop = asyncio.get_event_loop()
        task = loop.create_task(enqueue_data())
        connector.logger.debug('Created enqueue task %r', task)
        while (not task.done()) or (not data_queue.empty()):
            connector.logger.debug('Awaiting queue data')
            data = await data_queue.get()
            connector.logger.debug('Adding async result data')
            action_result.add_data(data)
            data_queue.task_done()

        task.result()

    async def consume_coroutine(self, connector, action_result, coroutine):
        connector.logger.debug('Consuming from coroutine %r', coroutine)
        result = await coroutine
        connector.logger.debug('Adding result data: %r', result)
        action_result.update_data(result)
        return result

    def consume_async_data(self, connector, action_result, data_source):
        if isasyncgen(data_source):
            coroutine = self.consume_async_generator(
                connector, action_result, data_source)
        else:
            coroutine = self.consume_coroutine(
                connector, action_result, data_source)

        connector.logger.debug('Creating event loop')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(coroutine)
        finally:
            connector.logger.debug('Closing event loop')
            loop.close()


class HandlerMixin(metaclass=ABCMeta):
    """
    An abstract mixin class that automates the delegation of action execution
    to the appropriately decorated class method.

    The current implementation of `phantom.base_connector.BaseConnector` is
    problematic to subclass, as Phantom blindly chooses the first such subclass
    as the connector implementation.
    This class sidesteps this issue at the cost of an extra superclass for
    connector implementations.
    """
    def __init__(self, *args, **kwargs):
        self.context = None
        self._state_context = None
        self.logger = logging.getLogger(self.__module__)
        # Setting the logging level to DEBUG will ensure all logging calls
        # are properly delegated to the appropriate
        # debug_print/error_print/save_progress calls.
        # The Phantom platform will still drop debug_print calls if the system
        # log level is not DEBUG.
        # In this case, the effective minimum log level is ERROR, but
        # save_progress calls will still be made for INFO.
        self.logger.setLevel(level=logging.DEBUG)
        log_handler = ConnectorLogHandler(connector=self)
        self.logger.addHandler(log_handler)

    @property
    def state(self):
        return self._state_context.data

    @property
    @lru_cache(maxsize=1)
    def config(self):
        return self.get_config()

    def get_vault_path(self, vault_id):
        try:
            vault_info_function = phantom.vault.vault_info
        except AttributeError:
            self.logger.debug('Using Phantom 4.8 vault interface')
            path_string = phantom.vault.Vault.get_file_path(vault_id)
        else:
            self.logger.debug('Using Phantom 4.10 vault interface')
            success, message, info = vault_info_function(vault_id=vault_id)
            if not success:
                raise RuntimeError(message)

            # All file entries for a vault ID will have the same file path
            path_string = info[0]['path']

        return Path(path_string).resolve()

    def open_vault_file(self, vault_id, mode='r'):
        self.logger.warning(
            '`open_vault_file` will be deprecated;'
            ' Use the `get_vault_path` and open the Path object directly'
        )
        file_path = self.get_vault_path(vault_id=vault_id)
        self.logger.debug(
            'Opening file path for vault ID %r: %r', vault_id, file_path)

        return file_path.open(mode)

    def handle_action(self, param):
        """
        Implements abstract method
        `phantom.base_connector.BaseConnector.handle_action`.

        Delegates execution to the appropriate action handler logic

        :param dict param: Parameter dictionary passed in by Phantom
        :return: The Phantom action result
        :rtype: phantom.action_result.ActionResult
        """
        action_identifier = self.get_action_identifier()
        action_handler = self.get_handler(action_identifier)
        unbound_method = action_handler.handler_method
        with StateContext(connector=self):
            return unbound_method(self, param)

    def open_state(self, path=None, *args, **kwargs):
        state_dir = Path(self.get_state_dir())
        if path is None:
            file_path = Path(self.get_state_file_path())
        else:
            file_path = state_dir.joinpath(path)

        resolved_path = file_path.resolve()

        # Raise ValueError if not subpath of state_dir
        resolved_path.relative_to(state_dir)

        return resolved_path.open(*args, **kwargs)

    def get_phantom_home(self):
        state_dir = Path(self.get_state_dir())
        # Expecting <PHANTOM_HOME>/local_data/app_states/<APP_ID>/
        *home_components, _, _, _ = state_dir.parts
        return Path(*home_components).resolve().absolute()

    def get_phantom_logs_path(self):
        components = ['var', 'log', 'phantom']
        privileged_logs = Path('/').joinpath(*components)
        if privileged_logs.exists():
            return privileged_logs

        phantom_home = self.get_phantom_home()
        unprivileged_logs = phantom_home.joinpath(*components)
        if unprivileged_logs.exists():
            return unprivileged_logs

        raise FileNotFoundError('Unable to find log directory')

    def get_logs_path(self):
        # The app doesn't have permission to write to the syslog apps directory
        # Use the app's state directory as a janky hack
        return Path(self.get_state_dir()).joinpath('logs')

    @classmethod
    def get_handlers(cls):
        """
        Get all action handler instances for this object
        """
        for action_identifier in ActionHandler.registered_handlers:
            try:
                yield cls.get_handler(action_identifier)
            except AttributeError:
                continue

    @classmethod
    def get_handler(cls, action_identifier):
        """
        Get the action handler for the provided action identifier

        The connector class is expected to have an `ActionHandler` member that
        is named after the action identifier.

        :param str action_identifier: The identifer of a handled action
        :return: The action handler for the identified action
        :rtype: function
        """
        target = getattr(cls, action_identifier)
        handler_set = ActionHandler.registered_handlers[action_identifier]
        if target in handler_set:
            return target

        raise AttributeError(
            f'{cls!r} has no handler for action identifier'
            f' {action_identifier}'
        )

    @classmethod
    def main(cls):
        """
        A direct copy of the logic provided by the app-creation wizard
        """
        import argparse
        import requests

        try:
            from pudb import set_trace as breakpoint
        except ImportError:
            from pdb import set_trace as breakpoint

        try:
            import debugpy
        except ImportError:
            pass
        else:
            if debugpy.is_client_connected():
                breakpoint = debugpy.breakpoint

        breakpoint()

        argparser = argparse.ArgumentParser()

        argparser.add_argument('input_test_json', help='Input Test JSON file')
        argparser.add_argument(
            '-u', '--username', help='username', required=False)
        argparser.add_argument(
            '-p', '--password', help='password', required=False)

        args = argparser.parse_args()
        session_id = None

        username = args.username
        password = args.password

        if username is not None and password is None:

            # User specified a username but not a password, so ask
            import getpass
            password = getpass.getpass("Password: ")

        if username and password:
            try:
                phantom_base_url = cls._get_phantom_base_url()
                login_url = f'{phantom_base_url}/login'

                print("Accessing the Login page")
                r = requests.get(login_url, verify=False)
                csrftoken = r.cookies['csrftoken']

                data = dict()
                data['username'] = username
                data['password'] = password
                data['csrfmiddlewaretoken'] = csrftoken

                headers = dict()
                headers['Cookie'] = 'csrftoken=' + csrftoken
                headers['Referer'] = login_url

                print("Logging into Platform to get the session id")
                r2 = requests.post(
                    login_url, verify=False, data=data, headers=headers)
                session_id = r2.cookies['sessionid']
            except Exception as e:
                print(
                    f"Unable to get session id from the platform. Error: {e}")
                exit(1)

        with open(args.input_test_json) as f:
            in_json = f.read()
            in_json = json.loads(in_json)
            print(json.dumps(in_json, indent=4))

            connector = cls()
            connector.print_progress_message = True

            if session_id is not None:
                in_json['user_session_token'] = session_id
                connector._set_csrf_info(csrftoken, headers['Referer'])

            ret_val = connector._handle_action(json.dumps(in_json), None)
            print(json.dumps(json.loads(ret_val), indent=4))

        exit(0)


registered_connectors = {}


def main_connector(connector_class):
    """
    This decorator automatically executes the decorated class's `main` method
    if the class is defined in the `__main__` module

    :param type connector_class: A Phantom app connector implementation
    """
    module = connector_class.__module__
    logger.debug(
        'Registering connector_class %r from module %r',
        connector_class,
        module,
    )
    registered_connectors.setdefault(module, set()).add(connector_class)
    logger.debug(
        'Registered connector %r from file %r', connector_class, __file__)

    if module != '__main__':
        return connector_class

    connector_class.main()
    return connector_class


def smart_connector(connector_class):
    """
    This decorator automatically subclasses the decorated class from
    each of `HandlerMixin` and `phantom.base_connector.BaseConnector` if it is
    not already a subclass.
    It also calls the `main_connector` decorator on the class to automatically
    execute the `main` method if the class is defined in the `__main__` module.

    Note: The `HandlerMixin` superclass is specified by default to facilitate
    IDE functionality, but is not necessary when using this decorator.

    :param type connector_class: A Phantom app connector implementation
    """
    new_superclasses = []
    for superclass in [HandlerMixin, BaseConnector]:
        if not issubclass(connector_class, superclass):
            new_superclasses.append(superclass)

    if not new_superclasses:
        return main_connector(connector_class)

    @wraps(connector_class.__init__)
    def init(connector, *args, **kwargs):
        super(HandlerMixin, connector).__init__(*args, **kwargs)
        super(connector_class, connector).__init__(*args, **kwargs)

    new_class = type(
        connector_class.__name__,
        (connector_class, *new_superclasses),
        {'__init__': init, '__original_class': connector_class},
    )

    new_class.__doc__ = connector_class.__doc__
    new_class.__module__ = connector_class.__module__
    return main_connector(new_class)


contains_map = {}


def contains(*args):
    def type_decorator(type_obj=None):
        if type_obj is None:
            type_obj = object()

        contains_map.setdefault(type_obj, [*args])
        return type_obj

    return type_decorator
