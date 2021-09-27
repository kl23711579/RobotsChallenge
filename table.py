class Table:
    def __init__(self, actions):
        self.robots = {}
        self.current_robot = ""
        self.actions = actions

    def receive_input(self, input_str):
        """ Receive command
        """
        input_strs = input_str.lower().split(" ")
        try: 
            self.actions[input_strs[0]](self, input_str)
        except Exception as e:
            print(e)
            pass

    def get_robots(self):
        return self.robots

    def set_current_robot(self, new_current_robot):
        self.current_robot = new_current_robot

    def get_current_robot(self):
        return self.current_robot


def place_robot(table, command = None):
    robots, current_robot = table.get_robots(), table.get_current_robot()
    pos1, pos2, direction = command.lower().split(" ")[1].split(",")
    pos1 = int(pos1)
    pos2 = int(pos2)
    is_vaild, err = check_pos(table, [pos1, pos2])
    if is_vaild:
        robot_num = str(len(robots)+1)
        robots[robot_num] = { "position": [pos1, pos2], "direction": direction }
        # set current robot if there do not have current robot
        if current_robot == "":
            table.set_current_robot("1")
    # else:
    #     print("\nERROR: %s" % (err))

def move(table, command = None):
    robots, current_robot = table.get_robots(), table.get_current_robot()
    if len(robots) >= 1:
        move_steps = { "north": [0, 1], "south": [0, -1], "west": [-1, 0], "east": [1, 0] }
        new_pos = [sum(x) for x in zip(robots[current_robot]["position"], move_steps[robots[current_robot]["direction"]]) ]
        is_vaild, err = check_pos(table, new_pos)
        if is_vaild:
            robots[current_robot]["position"] = new_pos
        # else:
        #     print("\nERROR: %s" % (err))

def change_robot(table, command = None):
    robots = table.get_robots()
    new_robot = command.lower().split(" ")[1]
    if int(new_robot) <= len(robots):
        table.set_current_robot(new_robot)
    # else:
        #     print("\nERROR: Robot not exist!!!")

def turn_left(table, command = None):
    robots, current_robot = table.get_robots(), table.get_current_robot()
    new_direction = { "north": "west", "west": "south", "south": "east", "east": "north" }
    if len(robots) >= 1:
        robots[current_robot]["direction"] = new_direction[robots[current_robot]["direction"]]

def turn_right(table, command = None):
    robots, current_robot = table.get_robots(), table.get_current_robot()
    new_direction = { "north": "east", "east": "south", "south": "west", "west": "north" }
    if len(robots) >= 1:
        robots[current_robot]["direction"] = new_direction[robots[current_robot]["direction"]]

def report(table, command = None):
    robots, current_robot = table.get_robots(), table.get_current_robot()
    if len(robots) >= 1:
        pos1, pos2 = robots[current_robot]["position"]
        direction = robots[current_robot]["direction"].upper()
        robot_number = len(robots)
        if robot_number == 1:
            print("\nOutput: %d, %d, %s" % (pos1, pos2, direction))
        else:
            print("\nOutput: There are %d robots in the table. Robot %s : %d, %d, %s" % (robot_number, current_robot, pos1, pos2, direction))

def check_pos(table, pos):
    robots = table.get_robots()
    # check is inside table
    if pos[0] < 0 or pos[1] < 0 or pos[0] > 4 or pos[1] > 4:
        error_msg = f"Position ({pos[0]}, {pos[1]}) is outside table."
        return [False, error_msg]
    else: # check is conflict with other robot
        for robot in robots.keys():
            if pos[0] == robots[robot]["position"][0] and pos[1] == robots[robot]["position"][1]:
                error_msg = f"Position ({pos[0]}, {pos[1]}) exist Robot {robot}."
                return [False, error_msg]

    return [True, ""]