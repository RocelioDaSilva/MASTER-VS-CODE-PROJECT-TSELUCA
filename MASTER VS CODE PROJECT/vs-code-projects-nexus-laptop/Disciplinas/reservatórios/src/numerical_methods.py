"""Generic numerical methods (e.g., Newton-Raphson)."""
from typing import Callable, Tuple

def newton_raphson(func: Callable[[float], float], deriv: Callable[[float], float],
                   x0: float, tol: float = 1e-8, max_iter: int = 100) -> Tuple[float, int]:
    x = x0
    for i in range(1, max_iter + 1):
        f = func(x)
        df = deriv(x)
        if abs(df) < 1e-14:
            raise ZeroDivisionError("Derivative too small in Newton-Raphson")
        x_new = x - f / df
        if abs(x_new - x) < tol:
            return x_new, i
        x = x_new
    return x, max_iter
