from scipy.integrate import quad
import numpy as np


def integrand(x, r):
    return np.sqrt(r**2 - x**2)


x_lower = 20
x_upper = 24.7
r = 25

area, error = quad(integrand, x_lower, x_upper, args=(r))
print(area)
