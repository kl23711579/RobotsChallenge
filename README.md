# Robot Challenge

## Execute

There are two ways to execute the code.

1. Read command from file
2. Input command

### Read command from file

```python
python3 main.py <file name>
```

I have put some file in the data folder.

#### Example

```python
python3 main.py "data/1.txt"
```

### Input command

```python
python3 main.py
```

Input commands in the terminal after execute the code.

## Test

There are two test code.

1. test_table.py
2. test_script.py

`test_table.py` performs unit test and it can be execute with command `python3 -m unittest discover`

`test_script.py` reads the files from testdata folder and execute the commands inside the text files.