from sparrow.version_ops import VersionControl

pkgname = "sparrow_tool"
pkgdir = "sparrow"
# vc = VersionControl(pkgname, pkgdir, version="0.1.6")
vc = VersionControl(pkgname, pkgdir, version=None)
vc.update_version()
vc.update_readme()
# os.system("yapf -i -r ./sparrow")

vc.upload_pypi()
