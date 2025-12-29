import unittest
import numpy as np
from stochastic_rates.calibration.curve import CurveCalibrator
from stochastic_rates.calibration.spline import NaturalCubicSpline1D

class TestCalibration(unittest.TestCase):
    def test_spline_interpolation(self):
        """Test natural cubic spline fitting."""
        x = [0, 1, 2, 3]
        y = [0, 1, 0, 1]
        spline = NaturalCubicSpline1D.fit(x, y)
        
        # Check interpolation at knots
        for xi, yi in zip(x, y):
            self.assertAlmostEqual(spline.evaluate(xi), yi)
            
        # Check natural boundary conditions (second derivative = 0)
        self.assertAlmostEqual(spline.evaluate_second_derivative(0), 0)
        self.assertAlmostEqual(spline.evaluate_second_derivative(3), 0)

    def test_curve_from_market(self):
        """Test CurveCalibrator initialization."""
        tenors = [0.1, 1.0, 5.0]
        spots = [0.01, 0.015, 0.02]
        cal = CurveCalibrator.from_market(tenors, spot_rates=spots)
        
        # Check t=0 extrapolation matches first spot
        self.assertAlmostEqual(cal.spot_rate(0), spots[0])
        # Check exact fit at grid points
        for t, r in zip(tenors, spots):
            self.assertAlmostEqual(cal.spot_rate(t), r)

    def test_flat_forward_extrapolation(self):
        """Test flat forward rate extrapolation beyond tensor."""
        tenors = [1.0, 2.0]
        spots = [0.01, 0.02]
        cal = CurveCalibrator.from_market(tenors, spot_rates=spots)
        
        t_max = 2.0
        f_max = cal.forward_rate(t_max)
        
        # Forward rate should be constant after t_max
        self.assertAlmostEqual(cal.forward_rate(3.0), f_max)
        self.assertAlmostEqual(cal.forward_rate(10.0), f_max)

if __name__ == "__main__":
    unittest.main()
