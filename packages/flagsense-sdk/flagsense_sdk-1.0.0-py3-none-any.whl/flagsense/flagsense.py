from .model.fs_user import FSUser
from .model.fs_flag import FSFlag
from .services.flagsense_service import FlagsenseService

_flagsense_service_map = {}


def create_service(sdk_id, sdk_secret, environment):
	if sdk_id not in _flagsense_service_map:
		_flagsense_service_map[sdk_id] = FlagsenseService(sdk_id, sdk_secret, environment)
	return _flagsense_service_map[sdk_id]


def user(userId, attributes=None):
	return FSUser(userId, attributes)


def flag(flagId, defaultKey=None, defaultValue=None):
	return FSFlag(flagId, defaultKey, defaultValue)


# Below methods can be used on instance returned from createService method
# initialization_complete()
# wait_for_initialization_complete()
# get_variation(fs_flag, fs_user)
