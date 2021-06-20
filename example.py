from sparrow.version_ops import VersionControl
from sparrow.color_str import rgb_string, YELLOW, GREEN

# vc = VersionControl("sparrow-tool")
# vc.update_version(1)

print(rgb_string("hello rgb string", YELLOW))

if __name__ == "__main__":
    print(rgb_string("hello rgb string", GREEN))
    print(rgb_string("hello rgb string", [1., 1., 1.]))
