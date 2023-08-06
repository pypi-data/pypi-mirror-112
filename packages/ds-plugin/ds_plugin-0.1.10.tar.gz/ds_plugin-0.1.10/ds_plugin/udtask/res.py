import logging
class Inherent(object):
    def print_self(self):
        logging.info(self.__class__.__name__)