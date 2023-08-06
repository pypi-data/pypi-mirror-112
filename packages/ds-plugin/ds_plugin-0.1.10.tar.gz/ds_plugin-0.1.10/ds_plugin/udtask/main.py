import os
import logging
from ds_plugin.common import io_utils
from ds_plugin.udtask.res import Inherent as inh_class

def main():
    os.environ['PYTHONUNBUFFERED'] = "1"
    logging.info("This is Udtask Main.py")
    inh = inh_class()
    inh.print_self()

    fs, path = io_utils.resolve_filesystem_and_path("hdfs://bigo-rt/user/bmlx/bmlx-unittest")

if __name__ == '__main__':
    main()