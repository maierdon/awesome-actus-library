import unittest
import numpy as np
import pandas as pd
from stochastic_rates.simulation import SimulationResult
from stochastic_rates.integration import simulation_to_reference_index, simulation_to_scenarios

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a dummy simulation result
        # T=1, M=2 (dt=0.5), I=2 paths
        self.times = np.array([0.0, 0.5, 1.0])
        self.rates = np.array([
            [0.01, 0.01],  # t=0
            [0.015, 0.02], # t=0.5
            [0.012, 0.025] # t=1.0
        ])
        self.sim = SimulationResult(times=self.times, rates=self.rates)

    def test_single_path_to_reference_index(self):
        """Test conversion of single path to ReferenceIndex."""
        ri = simulation_to_reference_index(
            self.sim,
            base_date="2025-01-01",
            market_code="YC_CHF",
            path=0,
            freq="6M" # 0.5 years
        )
        
        df = ri.data
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertEqual(df.iloc[0]['value'], 0.01)
        self.assertEqual(df.iloc[2]['value'], 0.012)
        # Check date generation
        self.assertEqual(df.iloc[0]['date'], "2025-01-01")

    def test_scenario_set_generation(self):
        """Test generation of multiple scenarios."""
        scen_set = simulation_to_scenarios(
            self.sim,
            base_date="2025-01-01",
            market_code="YC_CHF",
            freq="6M"
        )
        
        self.assertEqual(len(scen_set), 2)
        self.assertIn("SCEN_0000", scen_set.scenarios)
        self.assertIn("SCEN_0001", scen_set.scenarios)
        
        # Check content of path 1
        ri1 = scen_set.scenarios["SCEN_0001"]
        self.assertEqual(ri1.data.iloc[2]['value'], 0.025)

if __name__ == "__main__":
    unittest.main()
