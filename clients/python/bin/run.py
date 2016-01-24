#!/usr/bin/env python

import os, subprocess, sys

if len(sys.argv) < 2:
    print """
Incorrect number of args:
run.py module [arg0 arg1...]
"""
    sys.exit(1)

def ToClientModule(script, module):
    module_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(script),
            ".."
        )
    )
    sys.path.append(module_dir)
    return os.path.join(module_dir, module + ".py")

args = [ToClientModule(sys.argv[0], sys.argv[1])]
args.extend(sys.argv[2:])
# TODO(jsestrich) Add check that this is calling a client module
subprocess.check_call(args)
