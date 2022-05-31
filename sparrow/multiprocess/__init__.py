import os
from subprocess import Popen, PIPE
from pathlib import Path
from sparrow.multiprocess.config import Config


def run(cmd, **env):
    cmd = cmd.split(' ') if isinstance(cmd, str) else cmd
    p = Popen(cmd, cwd=str(Path(__file__).parent), env={**os.environ, **env})
    return p


def start_server():
    server_dir = os.path.dirname(os.path.realpath(__file__))

    p = run(f"python {server_dir}/server.py")
    print('pid:', p.pid)
    print(f"service start at {Config()}")
    p.communicate()
    return p


def stop_server(p: Popen):
    p.kill()
