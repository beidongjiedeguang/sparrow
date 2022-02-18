import numpy as np


class Sigmoid:
    def __init__(self):
        """A logistic sigmoid activation function."""

    def __str__(self):
        return "Sigmoid"

    @staticmethod
    def fn(z):
        return 1 / (1 + np.exp(-z))

    def grad(self, x):
        fn_x = self.fn(x)
        return fn_x * (1 - fn_x)


class ReLU:
    def __init__(self):
        """A rectified linear activation function."""

    def __str__(self):
        return "ReLU"

    @staticmethod
    def fn(z):
        return np.clip(z, 0, np.inf)

    @staticmethod
    def grad(x):
        return (x > 0).astype(int)

    @staticmethod
    def grad2(x):
        return np.zeros_like(x)


class LeakyReLU:
    """
    'Leaky' version of a rectified linear unit (ReLU).
    Notes
    -----
    Leaky ReLUs [*]_ are designed to address the vanishing gradient problem in
    ReLUs by allowing a small non-zero gradient when `x` is negative.
    Parameters
    ----------
    alpha: float
        Activation slope when x < 0. Default is 0.3.
    """

    def __init__(self, alpha=0.3):
        self.alpha = alpha

    def __str__(self):
        """Return a string representation of the activation function"""
        return "Leaky ReLU(alpha={})".format(self.alpha)

    def fn(self, z):
        _z = z.copy()
        _z[z < 0] = _z[z < 0] * self.alpha
        return _z

    def grad(self, x):
        out = np.ones_like(x)
        out[x < 0] *= self.alpha
        return out

    @staticmethod
    def grad2(x):
        return np.zeros_like(x)


class Tanh:
    def __init__(self):
        """A hyperbolic tangent activation function."""

    def __str__(self):
        """Return a string representation of the activation function"""
        return "Tanh"

    @staticmethod
    def fn(z):
        """Compute the tanh function on the elements of input `z`."""
        return np.tanh(z)

    @staticmethod
    def grad(x):
        return 1 - np.tanh(x) ** 2

    @staticmethod
    def grad2(x):
        tanh_x = np.tanh(x)
        return -2 * tanh_x * (1 - tanh_x**2)


class Affine:
    def __init__(self, slope=1, intercept=0):
        """
        An affine activation function.
        Parameters
        ----------
        slope: float
            Activation slope. Default is 1.
        intercept: float
            Intercept/offset term. Default is 0.
        """
        self.slope = slope
        self.intercept = intercept

    def __str__(self):
        """Return a string representation of the activation function"""
        return "Affine(slope={}, intercept={})".format(self.slope, self.intercept)

    def fn(self, z):
        return self.slope * z + self.intercept

    def grad(self, x):
        return self.slope * np.ones_like(x)

    @staticmethod
    def grad2(x):
        return np.zeros_like(x)


class Identity(Affine):
    def __init__(self, *args, **kwargs):
        """
        Identity activation function.
        Notes
        -----
        :class:`Identity` is just syntactic sugar for :class:`Affine` with
        slope = 1 and intercept = 0.
        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "Identity"


class ELU:
    def __init__(self, alpha=1.0):
        r"""
        An exponential linear unit (ELU).

        alpha : float
            Slope of negative segment. Default is 1.
        """
        self.alpha = alpha

    def __str__(self):
        return "ELU(alpha={})".format(self.alpha)

    def fn(self, z):
        """z if z > 0  else alpha * (e^z - 1)"""
        return np.where(z > 0, z, self.alpha * (np.exp(z) - 1))

    def grad(self, x):
        # 1 if x > 0 else alpha * e^(z)
        return np.where(x > 0, np.ones_like(x), self.alpha * np.exp(x))

    def grad2(self, x):
        # 0 if x > 0 else alpha * e^(z)
        return np.where(x >= 0, np.zeros_like(x), self.alpha * np.exp(x))


class Exponential:
    def __init__(self):
        """An exponential (base e) activation function"""

    def __str__(self):
        return "Exponential"

    @staticmethod
    def fn(z):
        return np.exp(z)

    @staticmethod
    def grad(x):
        return np.exp(x)

    @staticmethod
    def grad2(x):
        return np.exp(x)


class SELU:
    r"""
    A scaled exponential linear unit (SELU).
    """

    def __init__(self):
        self.alpha = 1.6732632423543772848170429916717
        self.scale = 1.0507009873554804934193349852946
        self.elu = ELU(alpha=self.alpha)

    def __str__(self):
        return "SELU"

    def fn(self, z):
        return self.scale * self.elu.fn(z)

    def grad(self, x):
        return np.where(
            x >= 0,
            np.ones_like(x) * self.scale,
            np.exp(x) * self.alpha * self.scale,
        )

    def grad2(self, x):
        return np.where(x > 0, np.zeros_like(x), np.exp(x) * self.alpha * self.scale)


class HardSigmoid:
    def __init__(self):
        """
        Notes
        -----
        The hard sigmoid is a piecewise linear approximation of the logistic
        sigmoid that is computationally more efficient to compute.
        """

    def __str__(self):
        return "Hard Sigmoid"

    @staticmethod
    def fn(z):
        return np.clip((0.2 * z) + 0.5, 0.0, 1.0)

    @staticmethod
    def grad(x):
        return np.where((x >= -2.5) & (x <= 2.5), 0.2, 0)

    @staticmethod
    def grad2(x):
        return np.zeros_like(x)


class SoftPlus:
    def __init__(self):
        """
        A softplus activation function.
        Notes
        -----
        In contrast to :class:`ReLU`, the softplus activation is differentiable
        everywhere (including 0). It is, however, less computationally efficient to
        compute.
        The derivative of the softplus activation is the logistic sigmoid.
        """

    def __str__(self):
        return "SoftPlus"

    @staticmethod
    def fn(z):
        return np.log(np.exp(z) + 1)

    @staticmethod
    def grad(x):
        exp_x = np.exp(x)
        return exp_x / (exp_x + 1)

    @staticmethod
    def grad2(x):
        exp_x = np.exp(x)
        return exp_x / ((exp_x + 1) ** 2)
