"""Run cmd in subprocess.run.

Some error checking is performed with goal of avoiding echo of secret info.
"""
import subprocess
import shlex
from logzero import logger

def run_secret_cmd(cmd):
    """run_secret_cmd

    Runs a command using subprocess.run with some error checking, but no command echo to
    to avoid revealing secret info.
    """
    cp = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if (cp.returncode):
        print("returncode: ", cp.returncode)
        print("stdout: ", cp.stdout)
        print("stderr: ", cp.stderr)
    return cp.returncode

def run_cmd(cmd):
    """run_cmd

    Runs a command using subprocess.run with some error checking
    """
    try:
        cp = subprocess.run(cmd, shell=True)
        return cp.returncode
    except Exception as exc:
        logger.info("%s", cmd)
        logger.error("\n%s", exc)
        return True
