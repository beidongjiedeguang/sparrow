from sparrow.version_ops import VersionControl
from git.repo import Repo


pkgname = "sparrow_tool"
pkgdir = "sparrow"
# vc = VersionControl(pkgname, pkgdir, version="0.2.3")
vc = VersionControl(pkgname, pkgdir, version=None)
old_version = vc.config['version']

vc.update_version()
new_version = vc.config['version']
vc.update_readme(license='MIT')
# os.system("black ./sparrow")
# vc.upload_pypi()

repo = Repo('.')
repo.index.add(["README*.md", "workflow.py", 'setup.*', 'sparrow/version-config.yaml'])
repo.index.commit(f"[Upgrade] Bump version ({old_version} -> {new_version})")
tag = f"v{new_version}"
repo.create_tag(tag)
remote = repo.remote()
remote.push(tag)
remote.push()
