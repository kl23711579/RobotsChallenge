import unittest
from table import Table, check_pos

class TestCheckPosMethods(unittest.TestCase):

    def test_no_robot_in_table(self):
        robots = {}
        is_vaild, err = check_pos(robots, [1, 2])
        self.assertTrue(is_vaild)

    def test_exist_robot_in_table(self):
        robots = {"1":{"position": [1,1], "direction": "east"}}
        is_vaild, err = check_pos(robots, [1, 2])
        self.assertTrue(is_vaild)

    def test_put_new_robot_conflict(self):
        robots = {"1":{"position": [1,1], "direction": "east"}}
        is_vaild, err = check_pos(robots, [1, 1])
        self.assertFalse(is_vaild)

    def test_put_new_robot_ouside_table_north(self):
        is_vaild, err = check_pos({}, [0, 5])
        self.assertFalse(is_vaild)

    def test_put_new_robot_ouside_table_south(self):
        is_vaild, err = check_pos({}, [0, -1])
        self.assertFalse(is_vaild)

    def test_put_new_robot_ouside_table_east(self):
        is_vaild, err = check_pos({}, [5, 0])
        self.assertFalse(is_vaild)

    def test_put_new_robot_ouside_table_west(self):
        is_vaild, err = check_pos({}, [-1, 0])
        self.assertFalse(is_vaild)
