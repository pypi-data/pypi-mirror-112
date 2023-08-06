import requests
import threading
import time

from .event_service import EventService
from .user_variant_service import UserVariantService
from flagsense.model.fs_variation import FSVariation
from flagsense.util.constants import Constants
from flagsense.util.flagsense_error import FlagsenseError
from flagsense.util.utility import Utility


class FlagsenseService:
	def __init__(self, sdkId, sdkSecret, environment):
		if not sdkId or not sdkSecret:
			raise FlagsenseError('Empty sdk params not allowed')
		
		self._lastUpdatedOn = 0
		self._environment = environment
		if not environment or environment not in Constants.ENVIRONMENTS:
			self._environment = 'PROD'
		
		self._headers = {
			Constants.HEADERS['AUTH_TYPE']: 'sdk',
			Constants.HEADERS['SDK_ID']: sdkId,
			Constants.HEADERS['SDK_SECRET']: sdkSecret
		}
		
		self._data = {
			'segments': None,
			'flags': None
		}
		
		self._event_service = EventService(self._headers, self._environment)
		self._user_variant_service = UserVariantService(self._data)
		self._start_data_poller()
	
	def initialization_complete(self):
		return self._lastUpdatedOn > 0
	
	def wait_for_initialization_complete(self):
		Utility.wait_until(self.initialization_complete)
	
	def get_variation(self, fs_flag, fs_user):
		variant = self._get_variant(fs_flag.flag_id, fs_user.user_id, fs_user.attributes, {
			'key': fs_flag.default_key,
			'value': fs_flag.default_value
		})
		return FSVariation(variant['key'], variant['value'])
	
	def _get_variant(self, flagId, userId, attributes, defaultVariant):
		try:
			if self._lastUpdatedOn == 0:
				raise FlagsenseError('Loading data')
			variant = self._user_variant_service.evaluate(userId, attributes, flagId)
			self._event_service.add_evaluation_count(flagId, variant['key'])
			return variant
		except Exception as err:
			# print(err)
			self._event_service.add_evaluation_count(flagId, defaultVariant['key'] if defaultVariant['key'] else 'default')
			self._event_service.add_errors_count(flagId)
			return defaultVariant
	
	def _start_data_poller(self):
		self._polling_thread = threading.Thread(target=self._run)
		self._polling_thread.setDaemon(True)
		if not self._is_polling_thread_running:
			self._polling_thread.start()
	
	@property
	def _is_polling_thread_running(self):
		return self._polling_thread.is_alive()
	
	def _run(self):
		try:
			while self._is_polling_thread_running:
				self._fetch_latest()
				time.sleep(Constants.DATA_REFRESH_INTERVAL)
		except Exception as err:
			# print(err)
			pass
	
	def _fetch_latest(self):
		# print('fetching data at: ' + time.ctime(time.time()))
		body = {
			'environment': self._environment,
			'lastUpdatedOn': self._lastUpdatedOn
		}
		
		try:
			response = requests.post(
				Constants.BASE_URL + 'fetchLatest',
				headers=self._headers,
				json=body,
				timeout=10
			)
		except Exception as err:
			# print(err)
			return
		
		if not response or response.status_code != 200 or not response.content:
			return
		
		jsonResponse = response.json()
		
		if 'lastUpdatedOn' in jsonResponse and 'segments' in jsonResponse and 'flags' in jsonResponse:
			self._data['segments'] = jsonResponse['segments']
			self._data['flags'] = jsonResponse['flags']
			self._lastUpdatedOn = jsonResponse['lastUpdatedOn']
