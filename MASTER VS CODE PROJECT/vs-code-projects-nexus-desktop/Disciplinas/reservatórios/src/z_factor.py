"""Z-factor calculation methods (Hall-Yarborough, Dranchuk & Abou-Kassem)."""
import math

DAK_COEFFS = {
    "A1": 0.3265, "A2": -1.0700, "A3": -0.5339, "A4": 0.01569, "A5": -0.05165,
    "A6": 0.5475, "A7": -0.7361, "A8": 0.1844, "A9": 0.1056, "A10": 0.6134, "A11": 0.7210,
}


def z_ideal() -> float:
    return 1.0


def hall_yarborough_z(ppr: float, tpr: float, tol: float = 1e-5, max_iter: int = 100):
    """Hall-Yarborough Newton-Raphson solver. Returns (Z, info)."""
    if tpr <= 0:
        raise ValueError("Tpr must be positive")
    t = 1.0 / tpr
    y = 0.001
    for it in range(1, max_iter + 1):
        a = -0.06125 * ppr * t * math.exp(-1.2 * (1.0 - t) ** 2)
        b = y * (1.0 + y + y ** 2 - y ** 3) / (1.0 - y) ** 3
        c = -((4.58 * t - 9.76) * t + 14.76) * t * y ** 2
        d = ((42.4 * t - 242.2) * t + 90.7) * t * y ** (2.18 + 2.82 * t)
        f = a + b + c + d

        db = (y ** 4 - 4.0 * y ** 3 + 4.0 * y ** 2 + 4.0 * y + 1.0) / (1.0 - y) ** 4
        dc = -2.0 * ((4.58 * t - 9.76) * t + 14.76) * t * y
        dd = (2.18 + 2.82 * t) * ((42.4 * t - 242.2) * t + 90.7) * t * y ** (1.18 + 2.82 * t)
        df = db + dc + dd

        if abs(df) < 1e-14:
            raise ZeroDivisionError("Derivative nearly zero in Hall-Yarborough")
        y_new = y - f / df
        if abs(y_new - y) < tol:
            y = y_new
            break
        y = y_new
    z = 0.06125 * ppr * t * math.exp(-1.2 * (1.0 - t) ** 2) / y
    return z, {"iterations": it, "y": y}


def dak_z_from_rhor(rhor: float, tpr: float) -> float:
    c = DAK_COEFFS
    a1 = c["A1"] + c["A2"] / tpr + c["A3"] / tpr ** 3 + c["A4"] / tpr ** 4 + c["A5"] / tpr ** 5
    a2 = c["A6"] + c["A7"] / tpr + c["A8"] / tpr ** 2
    a3 = c["A9"] * (c["A7"] / tpr + c["A8"] / tpr ** 2)
    a4 = c["A10"] / tpr ** 3
    a5 = c["A11"]
    return (1.0 + a1 * rhor + a2 * rhor ** 2 - a3 * rhor ** 5 +
            a4 * (1.0 + a5 * rhor ** 2) * rhor ** 2 * math.exp(-a5 * rhor ** 2))


def dranchuk_abou_kassem_z(ppr: float, tpr: float, tol: float = 1e-8, max_iter: int = 200):
    """Iterate on reduced density to compute DAK Z. Returns (Z, info)."""
    if tpr <= 0:
        raise ValueError("Tpr must be positive")
    rhor = max(1e-8, 0.27 * ppr / tpr)
    for it in range(1, max_iter + 1):
        z = dak_z_from_rhor(rhor, tpr)
        rhor_new = 0.5 * rhor + 0.5 * (0.27 * ppr / (z * tpr))
        if abs(rhor_new - rhor) < tol:
            rhor = rhor_new
            break
        rhor = rhor_new
    z = dak_z_from_rhor(rhor, tpr)
    return z, {"iterations": it, "rho_r": rhor}
