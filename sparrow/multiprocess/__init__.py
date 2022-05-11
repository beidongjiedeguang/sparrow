import os
from subprocess import Popen, PIPE
from pathlib import Path


def run(cmd, **env):
    cmd = cmd.split(' ') if isinstance(cmd, str) else cmd
    p = Popen(cmd, cwd=str(Path(__file__).parent), env={**os.environ, **env})
    return p


def start_server():
    server_dir = os.path.dirname(os.path.realpath(__file__))
    print("start server")
    p = run(f"python {server_dir}/server.py")
    print(p.returncode, p.pid)
    p.communicate()
    return p


def stop_server(p: Popen):
    p.kill()
