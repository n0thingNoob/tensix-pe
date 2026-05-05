import subprocess


def run(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check)
