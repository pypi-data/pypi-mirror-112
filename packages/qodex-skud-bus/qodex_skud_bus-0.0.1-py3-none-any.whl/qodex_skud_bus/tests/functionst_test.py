import unittest
from qodex_skud_bus import functions


class FunctionsTest(unittest.TestCase):
    def test_get_dict(self):
        list_name = [{'k11': 'a11', 'k12': 'a12'}, {'k21': 'a21', 'k22': 'a22'}]
        result = functions.get_point_dict(list_name, 'k12', 'a12')
        self.assertEqual(result, list_name[0])


if __name__ == '__main__':
    unittest.main()
