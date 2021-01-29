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
    try:
        cp = subprocess.run(cmd, shell=True)
        return cp.returncode
    except Exception as exc:
        logger.error("\n%s", exc)
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
