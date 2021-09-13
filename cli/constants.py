USAGE_MESSAGE = """ 
Group your json data on values defined by arbitraty number of keys. Unknown key will be ignored.

Example: 
    cat input.json | python nest.py key_1 key_2 ... 
    python nest.py input.json key_1 key_2 ...

"""

PARAM_HELP_MESSAGE = {
    "file": "Json file with data to process. You can also use stdin as file input",
    "group": "Arbitrary number of keys to group json data values. Unknown keys will be ignored",
}
