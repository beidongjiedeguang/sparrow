from sparrow.version_ops import VersionControl
from sparrow.color_str import rgb_string, YELLOW, GREEN
from sparrow.decorator import runtime
import time
# vc = VersionControl("sparrow-tool")
# vc.update_version(1)

print(rgb_string("hello rgb string", YELLOW))


@runtime(10)
def function(n):
    s = n
    time.sleep(0.1)
    return s

if __name__ == "__main__":
    print(rgb_string("hello rgb string", GREEN))
    print(rgb_string("hello rgb string", [1., 1., 1.]))
    function(5)
