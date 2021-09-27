class Table:
    def __init__(self):
        self.robots = {}
        self.current_robot = ""

    def receive_input(self, input_str):
        input_strs = input_str.lower().split(" ")
        if input_strs[0] == "place":
            self.place_robot(input_strs[1])
        elif len(self.robots) > 0: # there exist robots in table
            if input_strs[0] == "robot":
                self.change_robot(input_strs[1])
            elif input_strs[0] == "move":
                self.move()
            elif input_strs[0] == "left":
                self.turn_left()
            elif input_strs[0] == "right":
                self.turn_right()
            elif input_strs[0] == "report":
                self.report()
        #     else:
        #         print("\nERROR: INVALID COMMENT!!!")
        # else:
        #     print("\nERROR: NO ROBOTS ON TABLE!!!")

    def place_robot(self, input_str):
        pos1, pos2, direction = input_str.split(",")
        pos1 = int(pos1)
        pos2 = int(pos2)
        is_vaild, err = self.check_pos([pos1, pos2])
        if is_vaild:
            robot_num = str(len(self.robots)+1)
            self.robots[robot_num] = { "position": [pos1, pos2], "direction": direction }
            # set current robot if there do not have current robot
            if self.current_robot == "":
                self.current_robot = "1"
        # else:
        #     print("\nERROR: %s" % (err))

    def move(self):
        move_steps = { "north": [0, 1], "south": [0, -1], "west": [-1, 0], "east": [1, 0] }
        new_pos = [sum(x) for x in zip(self.robots[self.current_robot]["position"], move_steps[self.robots[self.current_robot]["direction"]]) ]
        is_vaild, err = self.check_pos(new_pos)
        if is_vaild:
            self.robots[self.current_robot]["position"] = new_pos
        # else:
        #     print("\nERROR: %s" % (err))

    def change_robot(self, new_robot):
        if int(new_robot) <= len(self.robots):
            self.current_robot = new_robot
        # else:
        #     print("\nERROR: Robot not exist!!!")

    def turn_left(self):
        new_direction = { "north": "west", "west": "south", "south": "east", "east": "north" }
        self.robots[self.current_robot]["direction"] = new_direction[self.robots[self.current_robot]["direction"]]

    def turn_right(self):
        new_direction = { "north": "east", "east": "south", "south": "west", "west": "north" }
        self.robots[self.current_robot]["direction"] = new_direction[self.robots[self.current_robot]["direction"]]

    def report(self):
        pos1, pos2 = self.robots[self.current_robot]["position"]
        direction = self.robots[self.current_robot]["direction"].upper()
        robot_number = len(self.robots)
        if robot_number == 1:
            print("\nOutput: %d, %d, %s" % (pos1, pos2, direction))
        else:
            print("\nOutput: There are %d robots in the table. Robot %s : %d, %d, %s" % (robot_number, self.current_robot, pos1, pos2, direction))

    def check_pos(self, pos):
        # check is inside table
        if pos[0] < 0 or pos[1] < 0 or pos[0] > 4 or pos[1] > 4:
            error_msg = f"Position ({pos[0]}, {pos[1]}) is outside table."
            return [False, error_msg]
        else: # chech is conflict with other robot
            for robot in self.robots.keys():
                if pos[0] == self.robots[robot]["position"][0] and pos[1] == self.robots[robot]["position"][1]:
                    error_msg = f"Position ({pos[0]}, {pos[1]}) exist Robot {robot}."
                    return [False, error_msg]

        return [True, ""]

if __name__ == '__main__':
    import sys
    t = Table()
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        with open(file_name, "r") as f:
            commands = [ x.strip() for x in f.readlines() ]
        
        for command in commands:
            print(command)
            t.receive_input(command)
    else:
        while True:
            input_str = input()
            t.receive_input(input_str)