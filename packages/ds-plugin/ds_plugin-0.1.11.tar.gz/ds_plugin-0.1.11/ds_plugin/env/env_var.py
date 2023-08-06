import os
import re
import logging
ENV_PATTERN = "[^\$]*(\$\{([0-9A-Z_]*)\}).*"
def substitute_env_variable(line):
    mth = re.match(ENV_PATTERN, line)
    logging.debug("line: %s", line)
    logging.debug("type(mth): %s", type(mth))
    if mth is not None and mth.group(0) == line:
        old = mth.group(1)
        new = os.environ[mth.group(2)] if mth.group(2) in os.environ else ""
        line = line.replace(old, new)
        return substitute_env_variable(line)
    return line


def init_env_variable(env_file):
    with open(env_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("export"):
                reals = line.split(' ')[1].split('=')
                var = reals[0]
                val = reals[1].rstrip('\n')
                val = substitute_env_variable(val)
                logging.debug("var: %s, val: %s" % (var, val))
                os.environ[var] = val
    logging.info("ENV: %s " % os.environ)