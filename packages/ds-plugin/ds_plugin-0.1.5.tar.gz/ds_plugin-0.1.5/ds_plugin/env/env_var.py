import os
def init_env_variable():
    with open("/opt/dolphinscheduler/conf/env/dolphinscheduler_env.sh", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("export"):
                reals = line.split(' ')[1].split('=')
                var = reals[0]
                val = reals[1]
                print ("var: %s, val: %s" % (var, val.rstrip('\n')))
                os.environ[var] = val.rstrip('\n')
    print ("ENV: %s " % os.environ)