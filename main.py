def check_pos(robots, pos):
    # check is inside table
    if pos[0] < 0 or pos[1] < 0 or pos[0] > 4 or pos[1] > 4:
        error_msg = f"Position ({pos[0]}, {pos[1]}) is outside table."
        return [False, error_msg]
    else: # chech is conflict with other robot
        for robot in robots.keys():
            if pos[0] == robots[robot]["position"][0] and pos[1] == robots[robot]["position"][1]:
                error_msg = f"Position ({pos[0]}, {pos[1]}) exist Robot {robot}."
                return [False, error_msg]

    return [True, ""]
    
if __name__ == '__main__':
    robots = {}
    current_robot = ""
    move_steps = { "north": [0, 1], "south": [0, -1], "west": [-1, 0], "east": [1, 0] }
    turn_left = { "north": "west", "west": "south", "south": "east", "east": "north" }
    turn_right = { "north": "east", "east": "south", "south": "west", "west": "north" }

    # input_str = input()
    while True:
        input_strs = input().lower().split(" ")
        if input_strs[0] == "place":
            pos1, pos2, direction = input_strs[1].split(",")
            pos1 = int(pos1)
            pos2 = int(pos2)
            is_vaild, err = check_pos(robots, [pos1, pos2])
            if is_vaild:
                robot_num = str(len(robots)+1)
                robots[robot_num] = { "position": [pos1, pos2], "direction": direction }
                # set current robot if there do not have current robot
                if current_robot == "":
                    current_robot = "1"
            else:
                print("\nERROR: %s" % (err))
        elif len(robots) > 0: # there exist robots in table
            if input_strs[0] == "robot":
                if int(input_strs[1]) <= len(robots):
                    current_robot = input_strs[1]
                else:
                    print("\nERROR: Robot not exist!!!")
            elif input_strs[0] == "move":
                new_pos = [sum(x) for x in zip(robots[current_robot]["position"], move_steps[robots[current_robot]["direction"]]) ]
                is_vaild, err = check_pos(robots, new_pos)
                if is_vaild:
                    robots[current_robot]["position"] = new_pos
                else:
                    print("\nERROR: %s" % (err))
            elif input_strs[0] == "left":
                robots[current_robot]["direction"] = turn_left[robots[current_robot]["direction"]]
            elif input_strs[0] == "right":
                robots[current_robot]["direction"] = turn_right[robots[current_robot]["direction"]]
            elif input_strs[0] == "report":
                pos1, pos2 = robots[current_robot]["position"]
                direction = robots[current_robot]["direction"].upper()
                robot_number = len(robots)
                if robot_number == 1:
                    print("\nOutput: %d, %d, %s" % (pos1, pos2, direction))
                else:
                    print("\nOutput: There are %d robots in the table. Robot %s : %d, %d, %s" % (robot_number, current_robot, pos1, pos2, direction))
            else:
                print("\nERROR: INVALID COMMENT!!!")
        else:
            print("\nERROR: NO ROBOTS ON TABLE!!!")
            pass

