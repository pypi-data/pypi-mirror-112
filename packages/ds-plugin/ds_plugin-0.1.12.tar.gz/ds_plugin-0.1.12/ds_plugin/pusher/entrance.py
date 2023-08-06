import os
import sys
import ds_plugin.pusher.test_main as py_main

def enter():
    json_string = "${parameters}"
    if json_string.startswith("$"):
        raise RuntimeError("entrance should have json_string")
    py_main.main(json_string)

if __name__ == '__main__':
    enter()