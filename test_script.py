if __name__ == "__main__":
    import os
    from io import StringIO
    from contextlib import redirect_stdout
    from table import Table

    # change dir to testdata
    os.chdir("testdata")
    # list all files inside testdata and remove .
    file_names = [ x for x in os.listdir() if x.endswith(".txt") ]
    print(file_names)

    for file_name in file_names:
        t = Table()
        with open(file_name, "r") as file:
            commands = [ x.strip() for x in file.readlines() ]
        
        # start with output is report
        outputs = []
        for i in range(len(commands)-1, -1, -1):
            if commands[i].startswith("Output:"):
                outputs.insert(0, commands.pop(i))

        output_index = 0
        for command in commands:
            if command.startswith("REPORT"):
                with redirect_stdout(StringIO()) as f:
                    t.receive_input(command)
                s = f.getvalue().strip()
                # check report from table is same as output in file
                assert s == outputs[output_index]
                output_index += 1
            else:
                t.receive_input(command)

            
        

    
