import unittest
from qodex_skud_bus.main import QodexSkudBus


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

    def test_get_locked_state(self):
        info = self.qsb.get_last_lock_info('EXTERNAL_GATE')
        response_must = {'last_change_timestamp': None, 'current': None}
        self.assertEqual(info, response_must)


if __name__ == '__main__':
    unittest.main()
