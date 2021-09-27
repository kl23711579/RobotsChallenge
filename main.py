
def main():
    import sys
    from table import Table, place_robot, change_robot, move, turn_left, turn_right, report
    actions = {
        "place": place_robot,
        "robot": change_robot,
        "move": move,
        "left": turn_left,
        "right": turn_right,
        "report": report
    }
    t = Table(actions)
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

if __name__ == '__main__':
    main()