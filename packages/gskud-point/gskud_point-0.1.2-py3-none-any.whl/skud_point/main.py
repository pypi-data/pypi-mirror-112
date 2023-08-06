import datetime
from skud_point import functions

class SkudPoint:
    def __init__(self, skud_sdk, point_number, request_current_state=None):
        self.skud_sdk = skud_sdk
        self.point_number = point_number
        self.last_states = {'ONLINE_NORMAL': {'last_change_timestamp': None,
                                              'current': None},
                            'ONLINE_LOCKED': {'last_change_timestamp': None,
                                              'current': None},
                            'ONLINE_UNLOCKED': {'last_change_timestamp': None,
                                              'current': None}}
        self.current_state = None
        if request_current_state:
            self.request_current_state()

    def set_point_locked(self):
        self.skud_sdk.set_point_locked(self.point_number)
        self.request_current_state()

    def set_point_unlocked(self):
        self.skud_sdk.set_point_unlocked(self.point_number)
        self.request_current_state()

    def set_point_normal(self):
        self.skud_sdk.set_point_normal(self.point_number)
        self.request_current_state()

    def set_current_state(self, state, *args, **kwargs):
        self.current_state = state

    def get_states_dict(self, *args, **kwargs):
        for state, info in self.last_states.items():
            if not info['last_change_timestamp']:
                info['last_change_timestamp'] = datetime.datetime(1997, 8, 24)
        return self.last_states

    def get_current_state(self, *args, **kwargs):
        return self.current_state

    def set_state(self, state):
        functions.update_last_state(self.last_states, state)

    def request_current_state(self):
        current_state = self.skud_sdk.get_point_status_parsed(self.point_number)
        self.set_current_state(current_state)
        self.set_state(current_state)
