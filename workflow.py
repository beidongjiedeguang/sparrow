import os
from sparrow.file_ops import rm
from sparrow.version_ops import VersionControl
pkgname = "sparrow-tool"
pkgdir = "sparrow"
vc = VersionControl(pkgname, pkgdir, version=None)
vc.update_readme("README.md")
vc.update_version(1)

rm('build', 'dist', 'eggs', 'sparrow_tool.egg-info')
# os.system("yapf -i -r ./sparrow")
os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')

rm('build', 'dist', 'eggs', 'sparrow_tool.egg-info')

