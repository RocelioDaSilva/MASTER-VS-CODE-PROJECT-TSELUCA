"""Gas viscosity correlations: Lee-González-Eakin (1966) and Lucas (1981)."""
import math


def lee_gonzalez_eakin_viscosity(T_R: float, P: float, Z: float, gamma_g: float) -> float:
    """Lee-González-Eakin (1966) gas viscosity correlation.

    Parameters
    ----------
    T_R    : reservoir temperature [°R]
    P      : reservoir pressure [psia]
    Z      : Z-factor (dimensionless)
    gamma_g: specific gravity relative to air (air = 1)

    Returns
    -------
    μg [cp]
    """
    M = 28.97 * gamma_g                         # molecular weight [lb/lb-mol]
    rho_lb_ft3 = P * M / (Z * 10.73 * T_R)     # gas density [lb/ft³]
    rho_gcc = rho_lb_ft3 / 62.4                 # gas density [g/cm³]
    K = (9.4 + 0.02 * M) * T_R ** 1.5 / (209.0 + 19.0 * M + T_R)
    X = 3.5 + 986.0 / T_R + 0.01 * M
    Y = 2.4 - 0.2 * X
    return K * math.exp(X * rho_gcc ** Y) * 1.0e-4  # cp


def lucas_viscosity(T_R: float, Tpc: float, Ppc: float,
                    gamma_g: float, P: float) -> float:
    """Lucas (1981) gas viscosity correlation with high-pressure correction.

    Parameters
    ----------
    T_R    : reservoir temperature [°R]
    Tpc    : (corrected) pseudo-critical temperature [°R]
    Ppc    : (corrected) pseudo-critical pressure [psia]
    gamma_g: specific gravity relative to air
    P      : reservoir pressure [psia]

    Returns
    -------
    μg [cp]
    """
    M = 28.97 * gamma_g  # molecular weight [lb/lb-mol]
    Tr = T_R / Tpc
    Pr = P / Ppc

    if Tr <= 0:
        raise ValueError("Pseudo-reduced temperature must be positive.")

    # Inverse viscosity-reducing parameter ξ (oilfield units)
    xi = Tpc ** (1.0 / 6.0) / (M ** 0.5 * Ppc ** (2.0 / 3.0))

    # Low-pressure (atmospheric) viscosity [cp]
    mu_1 = (
        0.807 * Tr ** 0.618
        - 0.357 * math.exp(-0.449 * Tr)
        + 0.340 * math.exp(-4.058 * Tr)
        + 0.018
    ) / xi * 1.0e-4

    # High-pressure correction — Lucas (1981) coefficients
    a1 = 1.245e-3; a2 = 5.1726; a3 = 0.3286
    a4 = 1.6553;  a5 = 1.2723; a6 = 0.4489
    a7 = 3.0578;  a8 = 37.7332; a9 = 1.7368; a10 = 2.2310

    A = a1 * math.exp(a2 * (1.0 - Tr ** (-a3)))
    B = A * (a4 * Tr - a5)
    C = a6 * math.exp(a7 * (1.0 - Tr ** (-a8))) / Tr
    D = a9 + a10 / Tr

    Pr_pow = Pr ** 1.3088
    inner = 1.0 + C * Pr ** D
    denom = B * Pr_pow + (1.0 / inner) if abs(inner) > 1e-15 else B * Pr_pow
    if abs(denom) < 1e-14:
        return mu_1
    mu_ratio = 1.0 + A * Pr_pow / denom
    return mu_1 * mu_ratio  # cp
