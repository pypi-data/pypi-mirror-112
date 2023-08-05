class Inherent(object):
    def print_self(self):
        print (self.__class__.__name__, flush=True)

    def print_self2(self):
        print (self.__class__.__name__)