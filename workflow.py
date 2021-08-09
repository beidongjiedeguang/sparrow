from sparrow.version_ops import VersionControl

pkgname = "sparrow-tool"
pkgdir = "sparrow"
# vc = VersionControl(pkgname, pkgdir, version="0.1.6")
vc = VersionControl(pkgname, pkgdir, version=None)
vc.update_version(1)
vc.update_readme("README.md")
# os.system("yapf -i -r ./sparrow")

vc.upload_pypi(pkgname)
