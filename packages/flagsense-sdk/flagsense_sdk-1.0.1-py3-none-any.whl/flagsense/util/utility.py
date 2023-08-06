import time


class Utility:
	@staticmethod
	def wait_until(condition, period=0.5):
		while True:
			if condition():
				return
			time.sleep(period)
	
	@staticmethod
	def wait_until_with_timeout(condition, period=0.5, timeout=10):
		mustEndAt = time.time() + timeout
		while time.time() < mustEndAt:
			if condition():
				return True
			time.sleep(period)
		return False
	
	@staticmethod
	def get_or_default(obj, key, defaultValue):
		if obj and key in obj:
			return obj[key]
		return defaultValue
