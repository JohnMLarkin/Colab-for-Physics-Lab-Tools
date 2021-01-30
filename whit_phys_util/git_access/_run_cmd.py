"""Run cmd in subprocess.run.

Some error logging is performed with goal of avoiding echo of secret info.
"""
import subprocess

def run_secret_cmd(cmd, verbose=False):
    """run_secret_cmd

    Runs a command using subprocess.run with some error logging, but no command echo to \
    avoid revealing secret info.
    """
    cp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (verbose and cp.stdout):
        print(cp.stdout.strip())
    if (cp.returncode) or (verbose and cp.stderr):
        print(cp.stderr.strip())
    return cp.returncode

def run_cmd(cmd, verbose=False):
    """run_cmd

    Runs a command using subprocess.run with some error logging
    """
    cp = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if (verbose and cp.stdout):
        print(cp.stdout.strip())
    if (cp.returncode) or (verbose and cp.stderr):
        print(cp.args.strip())
        print(cp.stderr.strip())
    return cp.returncode

