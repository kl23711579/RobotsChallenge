import unittest
from table import Table, check_pos, place_robot, move, change_robot, turn_right, turn_left, report
from unittest.mock import patch
from io import StringIO

class TestCheckPosMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_check_pos_with_no_robot_in_table(self):
        """ Check position in an empty table
        """
        robots = {}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = check_pos(t, [1, 2])
        self.assertTrue(is_vaild)

    def test_check_pos_exist_robot_in_table(self):
        """ TCheck position on the non-empty table
        """
        robots = {"1":{"position": [1,1], "direction": "east"}}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        is_vaild, err = check_pos(t, [1, 2])
        self.assertTrue(is_vaild)

    def test_check_pos_put_new_robot_conflict(self):
        """ Check position which exist other robot
        """
        robots = {"1":{"position": [1,1], "direction": "east"}}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        is_vaild, err = check_pos(t, [1, 1])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_north(self):
        """ Check position robot outside the north boundary
        """
        robots = {}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = check_pos(t, [0, 5])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_south(self):
        """ Check position robot outside the south boundary
        """
        robots = {}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = check_pos(t, [0, -1])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_east(self):
        """ Check position outside the east boundary
        """
        robots = {}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = check_pos(t, [5, 0])
        self.assertFalse(is_vaild)

    def test_check_pos_put_new_robot_ouside_table_west(self):
        """ Check position outside the west boundary
        """
        robots = {}
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = ""
        is_vaild, err = check_pos(t, [-1, 0])
        self.assertFalse(is_vaild)

class TestPlaceRobotMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_place_robot_in_empty_table(self):
        """ Test place robot in empty table
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table(self.actions)
        place_robot(t, "PLACE 0,0,NORTH")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_no_conflict(self):
        """ Test place two robots without confict
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        place_robot(t, "PLACE 0,0,NORTH")
        place_robot(t, "PLACE 3,2,EAST")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_confict(self):
        """ Test place two robots on same posistion
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table(self.actions)
        place_robot(t, "PLACE 0,0,NORTH")
        place_robot(t, "PLACE 0,0,NORTH")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_outside_table(self):
        """ Test place robot outside table
        """
        robots = {}
        t = Table(self.actions)
        place_robot(t, "PLACE -1,2,EAST")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("", t.current_robot)

class TestTableMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_place_robot_in_empty_table_command(self):
        """ Test place robot in empty table with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table(self.actions)
        t.receive_input("PLACE 0,0,NORTH")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_no_conflict_command(self):
        """ Test place two robots without confict with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.receive_input("PLACE 0,0,NORTH")
        t.receive_input("PLACE 3,2,EAST")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_with_confict_command(self):
        """ Test place two robots on same posistion with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"}
        }
        t = Table(self.actions)
        t.receive_input("PLACE 0,0,NORTH")
        t.receive_input("PLACE 0,0,NORTH")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_place_robot_outside_table_command(self):
        """ Test place robot outside table with command
        """
        robots = {}
        t = Table(self.actions)
        t.receive_input("PLACE -1,2,EAST")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("", t.current_robot)

    
    def test_receive_move_command_before_place_robot(self):
        """ Test receive MOVE command before place robot
        """
        robots = {}
        current_robot = ""
        t = Table(self.actions)
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_receive_left_command_before_place_robot(self):
        """ Test receive LEFT command before place robot
        """
        robots = {}
        current_robot = ""
        t = Table(self.actions)
        t.receive_input("LEFT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_reveive_right_command_before_place_robot(self):
        """ Test receive RIGHT command before place robot
        """
        robots = {}
        current_robot = ""
        t = Table(self.actions)
        t.receive_input("RIGHT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_reveive_change_command_before_place_robot(self):
        """ Test receive ROBOT command before place robot
        """
        robots = {}
        current_robot = ""
        t = Table(self.actions)
        t.receive_input("ROBOT 1")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)
    
    def test_reveive_report_command_before_place_robot(self):
        """ Test receive REPORT command before place robot
        """
        robots = {}
        current_robot = ""
        t = Table(self.actions)
        t.receive_input("REPORT")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual(current_robot, t.current_robot)

    def test_change_robot_with_command(self):
        """ Test ROBOT command
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("ROBOT 2")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("2", t.current_robot)

    def test_change_to_not_exist_robot_with_command(self):
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("ROBOT 3")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)
    
    def test_move_with_command(self):
        """
        test MOVE on first robot by command "MOVE"
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,1], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_with_confict_command(self):
        """ Test MOVE command with conflict
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_outside_table_command(self):
        """ Test MOVE robot outside table with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("MOVE")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_left_with_command(self):
        """ Test turn left with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "east"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("LEFT")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_turn_right_with_command(self):
        """ Test turn right with command
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "west"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("RIGHT")
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_command(self, m_stdout):
        """
        test report command with only one robot
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        t.receive_input("REPORT")
        assert m_stdout.getvalue().strip() == "Output: 0, 0, SOUTH"



    @patch('sys.stdout', new_callable=StringIO)
    def test_report_two_robot_command(self, m_stdout):
        """
        test report command with two robots
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [3,4], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "2"
        t.receive_input("REPORT")
        assert m_stdout.getvalue().strip() == "Output: There are 2 robots in the table. Robot 2 : 3, 4, EAST"


class TestChangeRobotMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_change_robot(self):
        """ Test change robot 
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        change_robot(t, "ROBOT 2")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("2", t.current_robot)

    def test_change_to_not_exist_robot(self):
        """ Test change non-exist robot
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [3,2], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        change_robot(t, "ROBOT 3")
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

class TestMoveMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

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
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        move(t)
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_with_confict(self):
        """ Test move robot with conflict
        """
        robots = {
            "1": {"position": [0,0], "direction": "north"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        move(t)
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

    def test_move_outside_table(self):
        """ Test move robot outside table
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        move(t)
        self.assertDictEqual(robots, t.robots)
        self.assertEqual("1", t.current_robot)

class TestTurnLeftMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_turn_left(self):
        """ Test turn left
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "east"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        turn_left(t)
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

class TestTurnRightMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    def test_turn_right(self):
        """ Test turn right
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [0,1], "direction": "east"}
        }
        new_robots = {
            "1": {"position": [0,0], "direction": "west"},
            "2": {"position": [0,1], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        turn_right(t)
        self.assertDictEqual(new_robots, t.robots)
        self.assertEqual("1", t.current_robot)

class TestReportMethods(unittest.TestCase):
    def setUp(self):
        self.actions = {
            "place": place_robot,
            "robot": change_robot,
            "move": move,
            "left": turn_left,
            "right": turn_right,
            "report": report
        }

    @patch('sys.stdout', new_callable=StringIO)
    def test_report(self, m_stdout):
        """
        test report function with only one robot
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "1"
        report(t)
        assert m_stdout.getvalue().strip() == "Output: 0, 0, SOUTH"

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_two_robots(self, m_stdout):
        """
        test report function with two robots
        """
        robots = {
            "1": {"position": [0,0], "direction": "south"},
            "2": {"position": [3,4], "direction": "east"}
        }
        t = Table(self.actions)
        t.robots = robots
        t.current_robot = "2"
        report(t)
        assert m_stdout.getvalue().strip() == "Output: There are 2 robots in the table. Robot 2 : 3, 4, EAST"

if __name__ == "__main__":
    unittest.main()