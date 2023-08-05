# import click

# @click.command()
# @click.option('--target', type=str, default='sg')
# def enter():
#     logging.info("target: %s" % target)
import os
import sys

def enter():
    if len(sys.argv) != 2:
        raise RuntimeError("entrance should has 1 argument!")

if __name__ == '__main__':
    enter()