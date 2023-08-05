import os
import logging
def init_env_variable(env_file):
    with open(env_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("export"):
                reals = line.split(' ')[1].split('=')
                var = reals[0]
                val = reals[1]
                logging.debug("var: %s, val: %s" % (var, val.rstrip('\n')))
                os.environ[var] = val.rstrip('\n')
    logging.info("ENV: %s " % os.environ)