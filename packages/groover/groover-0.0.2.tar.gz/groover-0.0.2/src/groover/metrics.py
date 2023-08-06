import numpy as np
import numpy.linalg as la


def cosine_similarity(a, b, epsilon=1e-8):
    a_axis = len(a.shape) - 1
    b_axis = len(b.shape) - 1
    ap = a + epsilon
    bp = b + epsilon

    return np.sum(ap * bp, axis=max(a_axis, b_axis)) / la.norm(ap, axis=a_axis) / la.norm(bp, axis=b_axis)


def rhythm_blur(a, n=3):
    axis = len(a.shape) - 1
    b = a.copy()
    for i in range(1, n):
        b += np.roll(a, i, axis=axis) * (n - i) / n
        b += np.roll(a, -i, axis=axis) * (n - i) / n

    return b


def rhythm_similarity(a, b, n=3):
    return cosine_similarity(rhythm_blur(a, n), rhythm_blur(b, n))
