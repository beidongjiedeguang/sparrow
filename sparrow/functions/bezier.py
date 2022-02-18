from .core import choose


def bezier(points):
    n = len(points) - 1

    def result(t):
        return sum(
            [
                ((1 - t) ** (n - k)) * (t**k) * choose(n, k) * point
                for k, point in enumerate(points)
            ]
        )

    return result
