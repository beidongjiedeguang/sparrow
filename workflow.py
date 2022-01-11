from sparrow.version_ops import VersionControl
from git import Repo

pkgname = "sparrow_tool"
pkgdir = "sparrow"
# vc = VersionControl(pkgname, pkgdir, version="0.2.3")
vc = VersionControl(pkgname, pkgdir, version=None)
vc.update_version()
vc.update_readme()
# os.system("yapf -i -r ./sparrow")
# vc.upload_pypi()

repo = Repo('.')
repo.index.add(["README*.md", "requirements.txt", "workflow.py", 'setup.*', 'sparrow/version-config.yaml'])
repo.index.commit(f"[Upgrade] Version bump to [{vc.config['version']}]")
repo.create_tag(f"{vc.config['version']}")
remote = repo.remote()
remote.push(f"{vc.config['version']}")
remote.push()
