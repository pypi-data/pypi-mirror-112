from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory


dummy_logger = getLogger(name=__name__)


class BaseConnector:
	def __init__(self):
		self.action_results = []
		self.tmp_dir = None

	def __enter__(self):
		self.tmp_dir = TemporaryDirectory()
		return self

	def __exit__(self, exc_type, exc_info, traceback):
		self.tmp_dir.cleanup()
		self.tmp_dir = None

	def add_action_result(self, action_result):
		self.action_results.append(action_result)
		return action_result

	def debug_print(self, message):
		dummy_logger.debug(message)

	def error_print(self, message):
		dummy_logger.error(message)

	def get_action_identifier(self):
		raise NotImplementedError()

	def save_progress(self, message):
		dummy_logger.info(message)

	def get_state_dir(self):
		path = Path(self.tmp_dir.name).joinpath('state')
		path.mkdir(exist_ok=True)
		return path

	def get_logs_path(self):
		path = Path(self.tmp_dir.name).joinpath('logs')
		path.mkdir(exist_ok=True)
		return path
