import unittest
import numpy as np
from stochastic_rates import create_model, CurveCalibrator

class TestModels(unittest.TestCase):
    def setUp(self):
        # Create a simple toy curve
        self.tenors = [0.1, 1, 5, 10]
        self.spots = [0.01, 0.015, 0.02, 0.025]
        self.cal = CurveCalibrator.from_market(self.tenors, spot_rates=self.spots)

    def test_vasicek_parameters(self):
        """Test Vasicek parameter validation."""
        with self.assertRaises(ValueError):
            create_model("vasicek", r0=0.01, a=-0.1, b=0.02, sigma=0.01)
        
        model = create_model("vasicek", r0=0.01, a=0.1, b=0.02, sigma=0.01)
        self.assertEqual(model.name, "vasicek")

    def test_cir_parameters(self):
        """Test CIR parameter validation."""
        with self.assertRaises(ValueError):
            create_model("cir", r0=-0.01, a=0.1, b=0.02, sigma=0.01)
            
        model = create_model("cir", r0=0.01, a=0.1, b=0.02, sigma=0.01)
        self.assertEqual(model.name, "cir")

    def test_ho_lee_calibration(self):
        """Test Ho-Lee consistent drift calibration."""
        model = create_model("ho_lee", r0=self.spots[0], sigma=0.01, calibrator=self.cal)
        
        # Theoretical ZCB price at t=0 must match calibration
        for T in [1.0, 5.0]:
            P_model = model.zcb_price(t=0, T=T)
            P_curve = self.cal.zcb_price(T)
            self.assertAlmostEqual(P_model, P_curve, places=7, 
                                   msg=f"Ho-Lee ZCB mismatch at T={T}")

    def test_hull_white_calibration(self):
        """Test Hull-White consistent drift calibration."""
        model = create_model("hull_white", r0=self.spots[0], a=0.05, sigma=0.01, calibrator=self.cal)
        
        # Theoretical ZCB price at t=0 must match calibration
        for T in [1.0, 5.0]:
            P_model = model.zcb_price(t=0, T=T)
            P_curve = self.cal.zcb_price(T)
            # Hull-White formula is exact, should match closely
            self.assertAlmostEqual(P_model, P_curve, places=7,
                                   msg=f"Hull-White ZCB mismatch at T={T}")

    def test_simulation(self):
        """Test basic simulation output shape."""
        model = create_model("vasicek", r0=0.01, a=0.1, b=0.02, sigma=0.01)
        sim = model.simulate(T=2.0, M=20, I=50)
        self.assertEqual(sim.rates.shape, (21, 50))
        self.assertEqual(sim.times.shape, (21,))

if __name__ == "__main__":
    unittest.main()
