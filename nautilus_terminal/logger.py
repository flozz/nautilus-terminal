import os

DEBUG = False,
if "NAUTILUS_TERMINAL_DEBUG" in os.environ:
    DEBUG = True

def log(*args):
    if not DEBUG:
        return
    print("\x1B[1;36m[Nautilus Terminal]\x1B[0m %s" % " ".join([str(item) for item in args]))
