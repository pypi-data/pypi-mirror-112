import atexit
import copy
import math
import requests
import threading
import time
import uuid

from flagsense.util.constants import Constants


class EventService:
	def __init__(self, headers, environment):
		self._data = {}
		self._errors = {}
		self._requestBodyMap = {}
		self._timeSlot = self._get_time_slot(time.time())
		
		self._headers = headers
		self._body = {
			'machineId': str(uuid.uuid4()),
			'sdkType': 'python',
			'environment': environment,
			'data': None,
			'errors': None,
			'time': self._timeSlot
		}
		
		if Constants.CAPTURE_EVENTS_FLAG:
			self._start_event_sender()
			atexit.register(self._register_shutdown_hook)
	
	def add_evaluation_count(self, flagId, variantKey):
		try:
			if not Constants.CAPTURE_EVENTS_FLAG:
				return
			
			currentTimeSlot = self._get_time_slot(time.time())
			if currentTimeSlot != self._timeSlot:
				self._refresh_data(currentTimeSlot)
			
			if flagId in self._data:
				if variantKey in self._data[flagId]:
					self._data[flagId][variantKey] = self._data[flagId][variantKey] + 1
				else:
					self._data[flagId][variantKey] = 1
			else:
				self._data[flagId] = {
					variantKey: 1
				}
		except Exception as err:
			# print(err)
			pass
	
	def add_errors_count(self, flagId):
		try:
			if not Constants.CAPTURE_EVENTS_FLAG:
				return
			
			currentTimeSlot = self._get_time_slot(time.time())
			if currentTimeSlot != self._timeSlot:
				self._refresh_data(currentTimeSlot)
			
			if flagId in self._data:
				self._data[flagId] = self._data[flagId] + 1
			else:
				self._data[flagId] = 1
		except Exception as err:
			# print(err)
			pass
	
	def _get_time_slot(self, datetime):
		return math.floor(datetime / Constants.EVENT_FLUSH_INTERVAL) * Constants.EVENT_FLUSH_INTERVAL * 1000
	
	def _register_shutdown_hook(self):
		self._refresh_data(self._get_time_slot(time.time()))
		self._send_events()
	
	def _check_and_refresh_data(self, currentTimeSlot):
		if currentTimeSlot == self._timeSlot:
			return
		self._refresh_data(currentTimeSlot)
	
	def _refresh_data(self, currentTimeSlot):
		self._body['time'] = currentTimeSlot
		self._body['data'] = self._data
		self._body['errors'] = self._errors
		
		self._requestBodyMap[currentTimeSlot] = copy.deepcopy(self._body)
		
		self._timeSlot = currentTimeSlot
		self._data = {}
		self._errors = {}
	
	def _start_event_sender(self):
		self._polling_thread = threading.Thread(target=self._run)
		self._polling_thread.setDaemon(True)
		if not self._is_polling_thread_running:
			self._polling_thread.start()
	
	@property
	def _is_polling_thread_running(self):
		return self._polling_thread.is_alive()
	
	def _run(self):
		time.sleep(Constants.EVENT_FLUSH_INITIAL_DELAY)
		try:
			while self._is_polling_thread_running:
				self._send_events()
				time.sleep(Constants.EVENT_FLUSH_INTERVAL)
		except Exception as err:
			# print(err)
			pass
	
	def _send_events(self):
		# print('sending events at: ' + time.ctime(time.time()))
		currentTimeSlot = self._get_time_slot(time.time())
		if currentTimeSlot != self._timeSlot:
			self._refresh_data(currentTimeSlot)
		
		timeKeys = list(self._requestBodyMap.keys())
		
		for timeKey in timeKeys:
			if timeKey in self._requestBodyMap:
				requestBody = self._requestBodyMap[timeKey]
				if requestBody:
					self._send_event(timeKey, requestBody)
	
	def _send_event(self, timeKey, requestBody):
		try:
			response = requests.post(
				Constants.EVENTS_BASE_URL + 'variantsData',
				headers=self._headers,
				json=requestBody,
				timeout=10
			)
		except Exception as err:
			# print(err)
			return
		
		if not response or response.status_code != 200:
			return
		
		del self._requestBodyMap[timeKey]
