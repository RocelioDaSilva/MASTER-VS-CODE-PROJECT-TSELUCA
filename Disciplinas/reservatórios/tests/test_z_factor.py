import sys
import os
import unittest

# Ensure src is on path
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..', 'src'))
sys.path.insert(0, SRC)

import z_factor
import corrections
from utils import f_to_r
import viscosity
import volumetric


class TestZFactorExample(unittest.TestCase):
    def test_example_values(self):
        # Example from report
        gamma = 0.70
        y_co2 = 0.05
        y_h2s = 0.10
        y_n2 = 0.0
        T_F = 160.0
        T_R = f_to_r(T_F)

        Tpc_prime, Ppc_prime = corrections.corrected_pseudocriticals(
            gamma, y_co2, y_h2s, y_n2, correction='wichert_aziz', pseudo_method='standing_dry'
        )

        Tpr = T_R / Tpc_prime
        P = 3000.0
        Ppr = P / Ppc_prime

        z_hy, info_hy = z_factor.hall_yarborough_z(Ppr, Tpr)
        z_dak, info_dak = z_factor.dranchuk_abou_kassem_z(Ppr, Tpr)

        # Basic sanity checks: Z should be positive and reasonably close between methods
        self.assertTrue(0.5 < z_hy < 1.2, msg=f"Z_HY out of range: {z_hy}")
        self.assertTrue(0.5 < z_dak < 1.2, msg=f"Z_DAK out of range: {z_dak}")
        self.assertAlmostEqual(z_hy, z_dak, delta=0.03)


class TestViscosity(unittest.TestCase):
    """Sanity checks for gas viscosity correlations (PDF example case)."""

    def setUp(self):
        # PDF example: T=150°F, γg=0.75, CO2=5%, H2S=10%, N2=0, P=3300 psia
        self.gamma_g = 0.75
        self.T_R = f_to_r(150.0)
        self.P = 3300.0
        Tpc, Ppc = corrections.corrected_pseudocriticals(
            self.gamma_g, 0.05, 0.10, 0.0,
            correction='wichert_aziz', pseudo_method='standing_dry'
        )
        self.Tpc = Tpc
        self.Ppc = Ppc
        Tpr = self.T_R / Tpc
        Ppr = self.P / Ppc
        self.Z, _ = z_factor.hall_yarborough_z(Ppr, Tpr)

    def test_lee_gonzalez_eakin_range(self):
        mu = viscosity.lee_gonzalez_eakin_viscosity(
            self.T_R, self.P, self.Z, self.gamma_g
        )
        # Gas viscosity at reservoir conditions: typically 0.01–0.05 cp
        self.assertTrue(0.01 < mu < 0.05, msg=f"LGE μg out of range: {mu}")

    def test_lucas_range(self):
        mu = viscosity.lucas_viscosity(
            self.T_R, self.Tpc, self.Ppc, self.gamma_g, self.P
        )
        self.assertTrue(0.01 < mu < 0.05, msg=f"Lucas μg out of range: {mu}")

    def test_lge_lucas_agreement(self):
        mu_lge = viscosity.lee_gonzalez_eakin_viscosity(
            self.T_R, self.P, self.Z, self.gamma_g
        )
        mu_luc = viscosity.lucas_viscosity(
            self.T_R, self.Tpc, self.Ppc, self.gamma_g, self.P
        )
        # Both methods should agree within 20%
        self.assertAlmostEqual(mu_lge, mu_luc, delta=0.2 * mu_lge)


class TestVolumetric(unittest.TestCase):
    """Sanity checks for Bg and Eg."""

    def setUp(self):
        self.gamma_g = 0.75
        self.T_R = f_to_r(150.0)
        self.P = 3300.0
        Tpc, Ppc = corrections.corrected_pseudocriticals(
            self.gamma_g, 0.05, 0.10, 0.0,
            correction='wichert_aziz', pseudo_method='standing_dry'
        )
        Tpr = self.T_R / Tpc
        Ppr = self.P / Ppc
        self.Z, _ = z_factor.hall_yarborough_z(Ppr, Tpr)

    def test_bg_bbl_scf_range(self):
        Bg = volumetric.gas_formation_volume_factor(
            self.Z, self.T_R, self.P, 'bbl_scf'
        )
        # Typical high-P gas: 0.001–0.01 bbl/scf
        self.assertTrue(1e-4 < Bg < 1e-2, msg=f"Bg (bbl/scf) out of range: {Bg}")

    def test_bg_ft3_bbl_consistency(self):
        Bg_ft3 = volumetric.gas_formation_volume_factor(
            self.Z, self.T_R, self.P, 'ft3_scf'
        )
        Bg_bbl = volumetric.gas_formation_volume_factor(
            self.Z, self.T_R, self.P, 'bbl_scf'
        )
        # 1 bbl = 5.61458 ft³
        self.assertAlmostEqual(Bg_ft3 / Bg_bbl, 5.61458, places=3)

    def test_eg_is_reciprocal_of_bg(self):
        Bg = volumetric.gas_formation_volume_factor(
            self.Z, self.T_R, self.P, 'bbl_scf'
        )
        Eg = volumetric.gas_expansion_factor(
            self.Z, self.T_R, self.P, 'scf_bbl'
        )
        self.assertAlmostEqual(Bg * Eg, 1.0, places=6)


if __name__ == '__main__':
    unittest.main()
