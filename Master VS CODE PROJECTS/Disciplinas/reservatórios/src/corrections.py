"""Pseudo-critical properties and contaminant corrections."""
import math

def pseudo_critical_standing_dry(gamma_g: float):
    """Standing (1977) for dry gas."""
    ppc = 677.0 + 15.0 * gamma_g - 37.5 * gamma_g ** 2
    tpc = 168.0 + 325.0 * gamma_g - 12.5 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_standing_wet(gamma_g: float):
    """Standing (1977) for wet gas."""
    ppc = 706.0 - 51.7 * gamma_g - 11.1 * gamma_g ** 2
    tpc = 187.0 + 330.0 * gamma_g - 71.5 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_sutton_wet(gamma_g: float):
    """Sutton for wet/condensate gas."""
    ppc = 169.2 + 349.5 * gamma_g - 74.0 * gamma_g ** 2
    tpc = 756.8 - 131.07 * gamma_g - 3.6 * gamma_g ** 2
    return tpc, ppc


def pseudo_critical_properties(gamma_g: float, method: str = "standing_dry"):
    method = method.lower().strip()
    if method == "standing_dry":
        return pseudo_critical_standing_dry(gamma_g)
    if method == "standing_wet":
        return pseudo_critical_standing_wet(gamma_g)
    if method == "sutton_wet":
        return pseudo_critical_sutton_wet(gamma_g)
    raise ValueError("Invalid pseudo-critical method")


def wichert_aziz(tpc: float, ppc: float, y_co2: float, y_h2s: float):
    """Wichert-Aziz correction."""
    s = y_co2 + y_h2s
    if s <= 0:
        return tpc, ppc
    d = math.sqrt(max(y_h2s, 0.0)) - (y_co2 ** 4)
    eps = 120.0 * (s ** 0.9 - s ** 1.6) + 15.0 * d
    tpc_corr = tpc - eps
    denom = tpc + y_h2s * (1.0 - y_h2s) * eps
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Denominator zero in Wichert-Aziz correction")
    ppc_corr = (ppc * tpc_corr) / denom
    return tpc_corr, ppc_corr


def carr_kobayashi_burrows(tpc: float, ppc: float, y_co2: float, y_h2s: float, y_n2: float):
    """Carr-Kobayashi-Burrows correction (simplified)."""
    tpc_corr = tpc - 80.0 * y_co2 + 130.0 * y_h2s - 250.0 * y_n2
    ppc_corr = ppc + 440.0 * y_co2 + 600.0 * y_h2s - 170.0 * y_n2
    if tpc_corr <= 0 or ppc_corr <= 0:
        raise ValueError("Invalid corrected pseudo-critical properties")
    return tpc_corr, ppc_corr


def corrected_pseudocriticals(gamma_g: float, y_co2: float, y_h2s: float, y_n2: float,
                              correction: str = "wichert_aziz", pseudo_method: str = "standing_dry"):
    tpc, ppc = pseudo_critical_properties(gamma_g, pseudo_method)
    correction = (correction or "").lower().strip()
    if correction in ("none", ""):
        return tpc, ppc
    if correction == "wichert_aziz" or correction == "wichert":
        return wichert_aziz(tpc, ppc, y_co2, y_h2s)
    if correction == "carr_kobayashi_burrows" or correction == "ckb":
        return carr_kobayashi_burrows(tpc, ppc, y_co2, y_h2s, y_n2)
    raise ValueError("Invalid correction method")
