import math
from packaging import version

try:
	import mmh3
except ImportError:
	from flagsense.lib import pymmh3 as mmh3

from flagsense.util.constants import Constants
from flagsense.util.flagsense_error import FlagsenseError
from flagsense.util.utility import Utility

UNSIGNED_MAX_32_BIT_VALUE = 0xFFFFFFFF


class UserVariantService:
	def __init__(self, data):
		self._data = data
	
	def evaluate(self, userId, attributes, flagId):
		if not flagId or not userId:
			raise FlagsenseError('Bad Request')
		
		if not attributes:
			attributes = {}
		
		if flagId not in self._data['flags']:
			raise FlagsenseError('Flag not found')
		flag = self._data['flags'][flagId]
		
		userVariantKey = self._get_user_variant_key(userId, attributes, flag)
		return {
			'key': userVariantKey,
			'value': flag['variants'][userVariantKey]['value']
		}
	
	def _get_user_variant_key(self, userId, attributes, flag):
		envData = flag['envData']
		if envData['status'] == 'INACTIVE':
			return envData['offVariant']
		
		if not self._matches_prerequisites(userId, attributes, envData['prerequisites']):
			return envData['offVariant']
		
		targetUsers = envData['targetUsers']
		if targetUsers and userId in targetUsers:
			return targetUsers[userId]
		
		targetSegmentsOrder = envData['targetSegmentsOrder']
		if targetSegmentsOrder:
			for targetSegment in targetSegmentsOrder:
				if self._is_user_in_segment(userId, attributes, targetSegment):
					return self._allocate_traffic_variant(userId, flag, envData['targetSegments'][targetSegment])
		
		return self._allocate_traffic_variant(userId, flag, envData['traffic'])
	
	def _matches_prerequisites(self, userId, attributes, prerequisites):
		if not prerequisites:
			return True
		
		for prerequisite in prerequisites:
			if not self._is_user_in_segment(userId, attributes, prerequisite):
				return False
		
		return True
	
	def _is_user_in_segment(self, userId, attributes, segmentId):
		if segmentId not in self._data['segments']:
			return False
		segment = self._data['segments'][segmentId]
		
		andRules = segment['rules']
		for andRule in andRules:
			if not self._matches_and_rule(userId, attributes, andRule):
				return False
		
		return True
	
	def _matches_and_rule(self, userId, attributes, orRules):
		for orRule in orRules:
			if self._matches_rule(userId, attributes, orRule):
				return True
		return False
	
	def _matches_rule(self, userId, attributes, rule):
		attributeValue = self._get_attribute_value(userId, attributes, rule['key'])
		if not attributeValue:
			return False
		
		try:
			type = rule['type']
			userMatchesRule = False
			
			if type == 'INT' or type == 'DOUBLE':
				userMatchesRule = self._matches_number_rule(rule, attributeValue)
			elif type == 'BOOL':
				userMatchesRule = self._matches_bool_rule(rule, attributeValue)
			elif type == 'STRING':
				userMatchesRule = self._matches_string_rule(rule, attributeValue)
			elif type == 'VERSION':
				userMatchesRule = self._matches_version_rule(rule, attributeValue)
			
			return userMatchesRule == rule['match']
		except Exception as err:
			# print(err)
			return False
	
	def _get_attribute_value(self, userId, attributes, key):
		if key == 'id':
			return userId
		
		if not attributes or key not in attributes:
			return None
		
		return attributes[key]
	
	def _matches_number_rule(self, rule, attributeValue):
		values = rule['values']
		operator = rule['operator']
		
		if operator == 'LT':
			return attributeValue < values[0]
		elif operator == 'LTE':
			return attributeValue <= values[0]
		elif operator == 'EQ':
			return attributeValue == values[0]
		elif operator == 'GT':
			return attributeValue > values[0]
		elif operator == 'GTE':
			return attributeValue >= values[0]
		elif operator == 'IOF':
			return attributeValue in values
		
		return False
	
	def _matches_bool_rule(self, rule, attributeValue):
		values = rule['values']
		operator = rule['operator']
		
		if operator == 'EQ':
			return attributeValue == values[0]
		
		return False
	
	def _matches_string_rule(self, rule, attributeValue):
		values = rule['values']
		operator = rule['operator']
		
		if operator == 'EQ':
			return attributeValue == values[0]
		elif operator == 'HAS':
			return values[0] in attributeValue
		elif operator == 'SW':
			return attributeValue.startswith(values[0])
		elif operator == 'EW':
			return attributeValue.endswith(values[0])
		elif operator == 'IOF':
			return attributeValue in values
		
		return False
	
	def _matches_version_rule(self, rule, attributeValue):
		values = rule['values']
		operator = rule['operator']
		
		if operator == 'LT':
			return version.parse(attributeValue) < version.parse(values[0])
		elif operator == 'LTE':
			return version.parse(attributeValue) <= version.parse(values[0])
		elif operator == 'EQ':
			return version.parse(attributeValue) == version.parse(values[0])
		elif operator == 'GT':
			return version.parse(attributeValue) > version.parse(values[0])
		elif operator == 'GTE':
			return version.parse(attributeValue) >= version.parse(values[0])
		elif operator == 'IOF':
			return attributeValue in values
		
		return False
	
	def _allocate_traffic_variant(self, userId, flag, traffic):
		if len(traffic) == 1:
			return list(traffic.keys())[0]
		
		bucketingId = userId + flag['id']
		variantsOrder = flag['variantsOrder']
		
		hashValue = mmh3.hash(bucketingId, flag['seed']) & UNSIGNED_MAX_32_BIT_VALUE
		ratio = float(hashValue) / Constants.MAX_HASH_VALUE
		bucketValue = math.floor(Constants.TOTAL_THREE_DECIMAL_TRAFFIC * ratio)
		
		endOfRange = 0
		for variant in variantsOrder:
			endOfRange += Utility.get_or_default(traffic, variant, 0)
			if bucketValue < endOfRange:
				return variant
		
		return variantsOrder[-1]
