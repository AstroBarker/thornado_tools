#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#
#  -------------------------
#  Author: Brandon Barker
#  -------------------------
# 
#  A simple run script for thornado to automate a few parts I keep forgetting.
#  Currently: write git hash and thornado standard out to a file.
#
# -----------------------------------------------------------------------------

import os
import subprocess

thornado_dir = os.environ["THORNADO_DIR"]
working_dir = os.getcwd()
usr = 'bbarker'
logFile = './Output/thornado.log'

# write the current git hash to logfile
ghash = subprocess.check_output(["git", "describe", "--abbrev=24", "--always"]).decode('ascii').strip()
print(f'Git hash: {ghash}\n')

with open(logFile,"w") as file:
    file.write(f'Git hash: {ghash}\n')

# cmd = 'echo ' + ghash + '> ' + logFile
# os.system(cmd)

os.chdir('./Executables')

cmd = './ApplicationDriver_' + usr + ' | tee -a .' + logFile
print(cmd)
os.system(cmd)

os.chdir('../')