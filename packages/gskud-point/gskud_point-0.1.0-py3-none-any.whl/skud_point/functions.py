import datetime


def update_last_state(last_states: dict, state: str, timestamp=datetime.datetime.now(), *args, **kwargs):
    last_states[state]['last_change_timestamp'] = timestamp
    last_states[state]['current'] = True
    for last_state, info_dict in last_states.items():
        if last_state != state:
            info_dict['current'] = False

