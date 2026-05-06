"""Gas volumetric properties: Formation Volume Factor (Bg) and Expansion Factor (Eg).

Standard conditions: Psc = 14.7 psia, Tsc = 519.67 °R (60 °F).
"""


def gas_formation_volume_factor(Z: float, T_R: float, P: float,
                                unit: str = "bbl_scf") -> float:
    """Gas Formation Volume Factor (Bg).

    Parameters
    ----------
    Z    : Z-factor
    T_R  : reservoir temperature [°R]
    P    : reservoir pressure [psia]
    unit : one of
           'bbl_scf'  → res bbl / scf   (≈ 0.00504 Z T/P)
           'ft3_scf'  → res ft³ / scf   (≈ 0.02829 Z T/P)
           'm3_m3'    → res m³ / sm³    (≈ 0.02829 Z T/P, same constant)

    Returns
    -------
    Bg in the requested unit
    """
    # Bg [res ft³/scf] = Z * T_R * Psc / (Tsc * P)
    # = Z * T_R * 14.7 / (519.67 * P) = 0.028269 * Z * T_R / P
    Bg_ft3_scf = 0.028269 * Z * T_R / P

    if unit == "bbl_scf":
        return Bg_ft3_scf / 5.61458   # 1 bbl = 5.61458 ft³
    elif unit == "m3_m3":
        # 1 ft³ ≈ 0.028317 m³; 1 scf ≈ 0.028317 sm³ → ratio preserved
        return Bg_ft3_scf             # numerically identical to ft³/scf
    else:                             # "ft3_scf"
        return Bg_ft3_scf


def gas_expansion_factor(Z: float, T_R: float, P: float,
                         unit: str = "scf_bbl") -> float:
    """Gas Expansion Factor (Eg = 1 / Bg).

    Parameters
    ----------
    Z    : Z-factor
    T_R  : reservoir temperature [°R]
    P    : reservoir pressure [psia]
    unit : one of
           'scf_bbl'  → scf / res bbl
           'scf_ft3'  → scf / res ft³
           'm3_m3'    → sm³ / res m³

    Returns
    -------
    Eg in the requested unit
    """
    if unit == "scf_bbl":
        Bg = gas_formation_volume_factor(Z, T_R, P, "bbl_scf")
    elif unit == "m3_m3":
        Bg = gas_formation_volume_factor(Z, T_R, P, "m3_m3")
    else:                  # "scf_ft3"
        Bg = gas_formation_volume_factor(Z, T_R, P, "ft3_scf")

    return 1.0 / Bg if abs(Bg) > 1e-15 else float("inf")
