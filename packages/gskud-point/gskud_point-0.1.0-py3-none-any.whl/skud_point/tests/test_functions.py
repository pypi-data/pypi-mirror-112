import unittest
import datetime
from skud_point import functions
from skud_point.main import SkudPoint


class FunctionsTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sk = SkudPoint(None, 3, False)

    def test_set_last_state(self):
        first_state = 'ONLINE_NORMAL'
        res = self.sk.get_states_dict()
        self.assertTrue(res[first_state]['last_change_timestamp'] == datetime.date(1997, 8, 24))
        timestamp = datetime.datetime.now()
        functions.update_last_state(self.sk.last_states, first_state, timestamp)
        last_states_submassive = self.sk.last_states[first_state]
        second_state = 'ONLINE_LOCKED'
        self.assertTrue(last_states_submassive['last_change_timestamp'] == timestamp)
        functions.update_last_state(self.sk.last_states, second_state,
                                    timestamp)
        last_states_submassive = self.sk.last_states[second_state]
        self.assertTrue(last_states_submassive['last_change_timestamp'] == timestamp,
                        last_states_submassive['current'] == True)




if __name__ == '__main__':
    unittest.main()