import os
from subprocess import Popen, PIPE
from pathlib import Path

__author__ = 'kunyuan'


def run(cmd, **env):
    # keeps printing output when testing
    cmd = cmd.split(' ') if isinstance(cmd, str) else cmd
    p = Popen(cmd, cwd=str(Path(__file__).parent), env={**os.environ, **env})
    p.communicate()
    return p.returncode

# install dependencies
dependencies = [
    'pytest',
    'numpy',
    'einops'
    # 'parameterized',
]

assert 0 == run('pip install {} --progress-bar off'.format(' '.join(dependencies)))
# install sparrow-tool
assert 0 == run('pip install -e .')

assert 0 == run('pytest tests')
