import unittest
from qodex_skud_bus.main import QodexSkudBus
from qodex_skud_bus.functions import get_point_dict
from qdk.main import QDK


class MainTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points_list = [
                                {'point_name': 'EXTERNAL_GATE', 'point_num': 2, 'point_type': 'EXTERNAL_GATE'},
                                {'point_name': 'INTERNAL_GATE', 'point_num': 1, 'point_type': 'EXTERNAL_GATE'},
                                {'point_name': 'INTERNAL_PHOTOCELL', 'point_num': 3, 'point_type': 'INTERNAL_PHOTOCELL'},
                                {'point_name': 'EXTERNAL_PHOTOCELL', 'point_num': 4, 'point_type': 'EXTERNAL_PHOTOCELL'},
        ]
        self.qsb = QodexSkudBus('192.168.100.109', 3312, self.points_list, skud_test_mode=True)
        self.qdk = QDK('localhost', 5000)
        self.qdk.make_connection()
        self.qdk.subscribe()

    def test_lock(self):
        point_name = 'EXTERNAL_GATE'
        self.qsb.lock_point(point_name)
        state = self.qsb.get_point_state(point_name)
        state_must = 'ONLINE_LOCKED'
        self.assertEqual(state, state_must)

    def test_qdk_lock(self):
        response = self.qdk.execute_method('lock_point', get_response=True, point_name_str='INTERNAL_GATE')
        response_must = {'status': True, 'point_name': 'INTERNAL_GATE', 'point_num': 1, 'command': 'lock_point'}
        self.assertEqual(response_must, response)

    def test_qdk_unlock(self):
        response = self.qdk.execute_method('unlock_point', get_response=True, point_name_str='EXTERNAL_GATE')
        response_must = {'status': True, 'point_name': 'EXTERNAL_GATE', 'point_num': 2, 'command': 'unlock_point'}
        self.assertEqual(response_must, response)

    def test_qdk_normal(self):
        response = self.qdk.execute_method('normal_point', get_response=True, point_name_str='EXTERNAL_GATE')
        response_must = {'status': True, 'point_name': 'EXTERNAL_GATE', 'point_num': 2, 'command': 'normal_point'}
        self.assertEqual(response_must, response)

    def test_get_point_state(self):
        response = self.qdk.execute_method('get_point_state', get_response=True, point_name_str='INTERNAL_PHOTOCELL')
        response_must = None
        self.assertEqual(response_must, response)

    def test_emulate_card_read(self):
        self.qdk.execute_method('emulate_card_read', get_response=False, course='external', card_num='FFFF000412')
        response = self.qdk.get_response()

if __name__ == '__main__':
    unittest.main()
