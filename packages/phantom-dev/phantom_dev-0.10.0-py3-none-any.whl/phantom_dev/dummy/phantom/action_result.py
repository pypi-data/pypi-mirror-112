class ActionResult:
	def __init__(self, param):
		self.data = {'parameters': param, 'data': []}

	def add_data(self, data):
		self.data['data'].append(data)

	def set_status(self, status, exc_info=None, exception=None):
		self.data['status'] = status
		if exc_info is None:
			return

		self.data.setdefault('exceptions', []).append(
			{'exc_info': exc_info, 'exception': exception})

	def get_data(self):
		return self.data['data']

	def set_summary(self, summary):
		self.data['summary'] = summary
