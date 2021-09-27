import unittest
from table import Table
from unittest.mock import patch
from io import StringIO

class TestTableMethods(unittest.TestCase):
    def test_check_pos_with_no_robot_in_table(self):
        robots = {}
        t = Table()
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = t.check_pos([1, 2])
        self.assertTrue(is_vaild)

    def test_check_pos_exist_robot_in_table(self):
        robots = {"1":{"position": [1,1], "direction": "east"}}
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        is_vaild, err = t.check_pos([1, 2])
        self.assertTrue(is_vaild)

    def test_check_pos_put_new_robot_conflict(self):
        robots = {"1":{"position": [1,1], "direction": "east"}}
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        is_vaild, err = t.check_pos([1, 1])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_north(self):
        robots = {}
        t = Table()
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = t.check_pos([0, 5])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_south(self):
        robots = {}
        t = Table()
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = t.check_pos([0, -1])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_east(self):
        robots = {}
        t = Table()
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = t.check_pos([5, 0])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_west(self):
        robots = {}
        t = Table()
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = t.check_pos([-1, 0])
        self.assertFalse(is_vaild)

    def test_place_robot_in_empty_table(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table()
        t.place_robot("0,0,north")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_no_conflict(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.place_robot("0,0,north")
        t.place_robot("3,2,east")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_confict(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table()
        t.place_robot("0,0,north")
        t.place_robot("0,0,north")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_outside_table(self):
        robots = {}
        t = Table()
        t.place_robot("-1,2,east")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("", t.current_robot)

    def test_reveive_move_command_before_place_robot(self):
        robots = {}
        current_robot = ""
        t = Table()
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_reveive_left_command_before_place_robot(self):
        robots = {}
        current_robot = ""
        t = Table()
        t.receive_input("LEFT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_reveive_right_command_before_place_robot(self):
        robots = {}
        current_robot = ""
        t = Table()
        t.receive_input("RIGHT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_reveive_change_command_before_place_robot(self):
        robots = {}
        current_robot = ""
        t = Table()
        t.receive_input("ROBOT 1")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)
    
    def test_reveive_report_command_before_place_robot(self):
        robots = {}
        current_robot = ""
        t = Table()
        t.receive_input("REPORT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_change_robot(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.change_robot("2")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("2", t.current_robot)

    def test_change_robot_with_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("ROBOT 2")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("2", t.current_robot)

    def test_change_to_not_exist_robot(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.change_robot("3")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_change_to_not_exist_robot_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("ROBOT 3")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move(self):
        """
        test move function with moving first robot 
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,1], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.move()
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_with_command(self):
        """
        test move function with moving first robot by command "MOVE"
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,1], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_with_confict(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.move()
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_with_confict_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_outside_table(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.move()
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_outside_table_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_left(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "east"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.turn_left()
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_left_with_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "east"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("LEFT")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_right(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "west"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.turn_right()
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_right_with_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "west"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("RIGHT")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report(self, m_stdout):
        """
        test report function with only one robot
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.report()
        assert m_stdout.getvalue().strip() == "Output: 0, 0, SOUTH"

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_command(self, m_stdout):
        """
        test report command with only one robot
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("REPORT")
        assert m_stdout.getvalue().strip() == "Output: 0, 0, SOUTH"

    @patch('sys.stdout', new_callable=StringIO)
    def test_report(self, m_stdout):
        """
        test report function with two robots
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [3,4], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "2"
        t.report()
        assert m_stdout.getvalue().strip() == "Output: There are 2 robots in the table. Robot 2 : 3, 4, EAST"

    @patch('sys.stdout', new_callable=StringIO)
    def test_report(self, m_stdout):
        """
        test report command with two robots
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [3,4], "direction": "east"}
        }
        t = Table()
        t.robots = robots
        t.current_robot = "2"
        t.receive_input("REPORT")
        assert m_stdout.getvalue().strip() == "Output: There are 2 robots in the table. Robot 2 : 3, 4, EAST"

if __name__ == "__main__":
    unittest.main()