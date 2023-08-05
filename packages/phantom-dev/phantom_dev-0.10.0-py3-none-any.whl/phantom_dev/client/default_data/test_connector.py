from logging import getLogger
from unittest import mock

from pytest import fixture, fail

from connector import Connector


logger = getLogger(name=__name__)


NULL_VALUE = object()


@fixture(params=[42, 69, 13.37, -5, 0])
def numeric_value(request):
	return float(request.param)

@fixture(params=['foo', 'bar', 'baz'])
def text_value(request):
	return request.param

@fixture(params=[True, False])
def bool_value(request):
	return request.param

@fixture(params=[NULL_VALUE, 420.69])
def optional_numeric(request):
	return request.param

@fixture(params=[NULL_VALUE, 'optional'])
def optional_text(request, text_value):
	return request.param

@fixture(params=[NULL_VALUE, True, False])
def optional_bool(request, text_value):
	return request.param

@fixture
def expected_result(
		request,
		numeric_value,
		text_value,
		bool_value,
		optional_numeric,
		optional_text,
		optional_bool
):
	if optional_numeric is NULL_VALUE:
		optional_numeric = 42.69

	if optional_text is NULL_VALUE:
		optional_text = 'spam'

	if optional_bool is NULL_VALUE:
		optional_bool = False

	return [
		{
			'name': 'required_number',
			'value': numeric_value,
			'type': 'float',
			'context': 'None',
		},
		{
			'name': 'required_str',
			'value': text_value,
			'type': 'str',
			'context': 'None',
		},
		{
			'name': 'required_bool',
			'value': bool_value,
			'type': 'bool',
			'context': 'None',
		},
		{
			'name': 'optional_number',
			'value': optional_numeric,
			'type': 'float',
			'context': 'None',
		},
		{
			'name': 'optional_str',
			'value': optional_text,
			'type': 'str',
			'context': 'None',
		},
		{
			'name': 'optional_bool',
			'value': optional_bool,
			'type': 'bool',
			'context': 'None',
		},
	]

@fixture
def connector(request):
	connector = Connector()
	state = {}
	with mock.patch.object(connector, 'logger', logger):
		with mock.patch.object(Connector, 'state', state):
			yield connector

def test_dummy_action(
		connector,
		numeric_value,
		text_value,
		bool_value,
		optional_numeric,
		optional_text,
		optional_bool,
		expected_result
):
	sort_key = lambda x: x['name']
	optionals = {
		'optional_number': optional_numeric,
		'optional_str': optional_text,
		'optional_bool': optional_bool,
	}
	optionals = {k: v for k, v in optionals.items() if v is not NULL_VALUE}
	result = list(connector.dummy_action(
		numeric_value, text_value, bool_value, **optionals))

	sorted_result = sorted(result, key=sort_key)
	sorted_expected_result = sorted(expected_result, key=sort_key)
	assert sorted_result == sorted_expected_result
	assert connector.state['last_data'] == result[-1]


def test_dummy_async(connector):
	concurrency = 100
	sleep = 0.1
	with mock.patch.object(
			connector, 'get_action_identifier', lambda: 'dummy_async'):
		connector.handle_action({'concurrency': concurrency, 'sleep': sleep})

	result, = connector.action_results
	assert len(result.data['data']) == concurrency
	assert result.data['summary']['count'] == concurrency
