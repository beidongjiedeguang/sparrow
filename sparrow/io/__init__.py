from .core import *
from .ops import *
from subprocess import Popen, PIPE
from pathlib import Path


def run(cmd, **env):
    cmd = cmd.split(" ") if isinstance(cmd, str) else cmd
    p = Popen(cmd, cwd=str(Path(__file__).parent), env={**os.environ, **env})
    p.communicate()
    return p.returncode
