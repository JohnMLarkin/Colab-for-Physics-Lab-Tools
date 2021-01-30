"""Run cmd in subprocess.run.

Some error logging is performed with goal of avoiding echo of secret info.
"""
import subprocess

def run_secret_cmd(cmd):
    """run_secret_cmd

    Runs a command using subprocess.run with some error logging, but no command echo to
    to avoid revealing secret info.
    """
    cp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (cp.returncode):
        print(cp.stderr)
    else:
        print(cp.stdout)
    return cp.returncode

def run_cmd(cmd):
    """run_cmd

    Runs a command using subprocess.run with some error logging
    """
    cp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (cp.returncode):
        print(cp.args)
        print(cp.stderr)
    else:
        print(cp.stdout)
    return cp.returncode

