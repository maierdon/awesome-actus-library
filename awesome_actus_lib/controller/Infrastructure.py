import json

import pandas as pd
import requests

from ..models.cashFlowStream import CashFlowStream
from ..models.contract_terms_generated import *
from ..models.contractModel import ContractModel
from ..models.portfolio import Portfolio


class ActusService:
    """
    Handles simulation of ACTUS portfolios via direct event generation (/eventsBatch).
    """

    def __init__(self, serverURL: str, externalRiskService: bool = False):
        self.serverURL = serverURL.rstrip("/")
        self.externalRiskService = externalRiskService

    def generateEvents(self, portfolio, riskFactors=None):
        """
        Calls the /eventsBatch endpoint to generate event schedules.

        Args:
            portfolio (Portfolio): A portfolio of ACTUS contract objects.
            riskFactors (list or None): Optional list of risk factor dicts. If None, sends empty list.

        Returns:
            dict: JSON response from the ACTUS engine.
        """
        # Normalize input
        if isinstance(portfolio, ContractModel):
            portfolio = Portfolio([portfolio])
        elif not isinstance(portfolio, Portfolio):
            raise TypeError("Expected a ContractModel or Portfolio instance")
        
        contract_dicts = []

        for contract in portfolio.contracts:
            contract_data = contract.to_dict()
            for key, value in contract_data.items():
                # print(f"{key}: {type(value)}")
                if (
                    isinstance(value, str)
                    and len(value) == 10
                    and value.count("-") == 2
                ):
                    contract_data[key] = value + "T00:00:00"
            contract_dicts.append(contract_data)

        # Convert RiskFactor instances to JSON
        serialized_risk_factors = []
        if riskFactors:
            if not isinstance(riskFactors, list):
                riskFactors = [riskFactors]
            self._validate_rate_reset_risk_factor_coverage(portfolio, riskFactors)
            for rf in riskFactors:
                if hasattr(rf, "to_json") and callable(rf.to_json):
                    serialized_risk_factors.append(rf.to_json())
                elif isinstance(rf, dict):
                    serialized_risk_factors.append(rf)
                else:
                    raise TypeError(f"Invalid risk factor type: {type(rf)}. Must be a RiskFactor or dict.")
        
        # DEBUG
        # print(serialized_risk_factors)
        payload = {
            "contracts": contract_dicts,
            "riskFactors": serialized_risk_factors
        }
        # print(f"[DEBUG] Sending payload:{payload} to /eventsBatch:")
        # print("\n[DEBUG] curl command to test manually:\n")
        # print(
        #     "curl -v -H \"Content-Type: application/json\" -X POST "
        #     f"-d '{json.dumps(payload)}' {self.serverURL}/eventsBatch"
        # )

        response = requests.post(
            url=f"{self.serverURL}/eventsBatch",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        response.raise_for_status()
        # debug:
        # print(response.json())
        result = response.json()
        return CashFlowStream(portfolio=portfolio, riskFactors=riskFactors, raw_response=result)
    
    @staticmethod
    def extract_required_risk_factors(portfolio):
        required_rfs = set()
        for contract in portfolio.contracts:
            for term in contract.terms.values():
                if isinstance(term, RiskFactorReferenceTerm):
                    required_rfs.add(term.value)
        return required_rfs
    
    def _validate_rate_reset_risk_factor_coverage(self, portfolio: Portfolio, riskFactors: list):
        rf_map = {rf.marketObjectCode: rf for rf in riskFactors if hasattr(rf, "marketObjectCode") and hasattr(rf, "_data")}
        # print("[DEBUG] Running rate reset risk factor coverage validation")
        for contract in portfolio.contracts:
            contract_id = contract.terms.get("contractID", None)
            mkt_code = contract.terms.get("marketObjectCodeOfRateReset", None)
            anchor_date_str = contract.terms.get("cycleAnchorDateOfRateReset", None)

            # unwrap term values if present
            contract_id = contract_id.value if contract_id else "<unknown>"
            mkt_code = mkt_code.value if mkt_code else None
            anchor_date_str = anchor_date_str.value if anchor_date_str else None
            # print(f"[DEBUG] Before if cntid:{contract_id}, mktcode:{mkt_code}, ancdat:{anchor_date_str}")
            if mkt_code and anchor_date_str:
                # print("[DEBUG] After if")
                rf = rf_map.get(mkt_code)
                if rf is None:
                    raise ValueError(f"Contract '{contract_id}' references missing risk factor '{mkt_code}'")

                try:
                    rf_dates = list(pd.to_datetime(rf._data["date"]).dt.date)
                except Exception:
                    raise ValueError(f"Risk factor '{mkt_code}' for contract '{contract_id}' has invalid or missing date data")
                # print("HELLO WORLD")
                anchor_date = pd.to_datetime(anchor_date_str).date()
                # print(f"[DEBUG] Anchor date = {anchor_date}, RF dates = {[str(d) for d in rf_dates]}")
                if not any(d <= anchor_date for d in rf_dates):
                    raise ValueError(
                        f"Risk factor '{mkt_code}' does not cover required rate reset anchor date (cycleAnchorDateOfRateReset): {anchor_date} "
                        f"for contract '{contract_id}'"
                    )



    def generateEventsWithExternalRisk(self, portfolio, scenarioID, riskService, simulateTo="2030-01-01T00:00:00", monitoringTimes=None):
        if not self.externalRiskService:
            raise RuntimeError("generateEventsWithExternalRisk() called but externalRiskService=False")
        # Normalize input
        if isinstance(portfolio, ContractModel):
            portfolio = Portfolio([portfolio])
        elif not isinstance(portfolio, Portfolio):
            raise TypeError("Expected a ContractModel or Portfolio instance")

        # Step 1: Check if scenario exists
        scenario_url = f"{riskService.serverURL}/findScenario/{scenarioID}"
        response = requests.get(scenario_url)
        if response.status_code != 200:
            raise ValueError(f"Scenario '{scenarioID}' does not exist in the RiskService")

        scenario_data = response.json()
        scenario_rfs = {rf["riskFactorID"] for rf in scenario_data.get("riskFactorDescriptors", [])}

        # Step 2: Validate risk factors referenced in the portfolio
        required_rfs = self.extract_required_risk_factors(portfolio)
        missing = required_rfs - scenario_rfs
        if missing:
            raise ValueError(f"The following risk factors are missing from scenario '{scenarioID}': {', '.join(missing)}")

        # Step 3: Full contract payload (not just contract IDs)
        contract_dicts = []
        for contract in portfolio.contracts:
            contract_data = contract.to_dict()
            for key, value in contract_data.items():
                if isinstance(value, str) and len(value) == 10 and value.count("-") == 2:
                    contract_data[key] = value + "T00:00:00"
            contract_dicts.append(contract_data)

        # Step 4: Build full scenarioSimulation payload
        payload = {
            "contracts": contract_dicts,
            "scenarioDescriptor": {
                "scenarioID": scenarioID,
                "scenarioType": "scenario"
            },
            "simulateTo": simulateTo,
            "monitoringTimes": monitoringTimes or []
        }

        response = requests.post(
            url=f"{self.serverURL}/rf2/scenarioSimulation",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        result = response.json()

        return CashFlowStream(portfolio=portfolio, riskFactors=None, raw_response=result)




class PublicActusService(ActusService):
    def __init__(self):
        super().__init__(
            serverURL="https://dadfir3-app.zhaw.ch/",
            externalRiskService=False
        )


class RiskService:
    """
    Python client for interacting with the ACTUS RiskService API.
    Allows uploading, deleting, and querying risk factors and scenarios.
    """

    def __init__(self, serverURL: str):
        self.serverURL = serverURL.rstrip("/")

    # ---------- Reference Indexes ----------

    def upload_reference_index(self, risk_factor, riskFactorID: str):
        """
        Uploads a ReferenceIndex to the RiskService using its to_json() and injecting riskFactorID.
        """
        rf_data = risk_factor.to_json()
        rf_data["riskFactorID"] = riskFactorID

        
        # print("[DEBUG] Uploading risk factor with payload:")
        # print(json.dumps(rf_data, indent=2))

        response = requests.post(
            url=f"{self.serverURL}/addReferenceIndex",
            headers={"Content-Type": "application/json"},
            data=json.dumps(rf_data)
        )
        response.raise_for_status()
        print(response.text)
        return response.status_code


    def delete_reference_index(self, riskFactorID: str):
        """
        Deletes a specific ReferenceIndex from the RiskService.
        """
        response = requests.delete(f"{self.serverURL}/deleteReferenceIndex/{riskFactorID}")
        response.raise_for_status()
        return response.status_code

    def find_all_reference_indexes(self):
        """
        Returns all ReferenceIndexes stored in the RiskService.
        """
        response = requests.get(f"{self.serverURL}/findAllReferenceIndexes")
        response.raise_for_status()
        return response.json()

    def find_reference_index(self, riskFactorID: str):
        """
        Returns a specific ReferenceIndex by riskFactorID.
        """
        response = requests.get(f"{self.serverURL}/findReferenceIndex/{riskFactorID}")
        response.raise_for_status()
        return response.json()

    # ---------- Scenarios ----------

    def create_scenario(self, scenarioID: str, riskFactorDescriptors: list[dict]):
        """
        Creates a scenario by linking riskFactorIDs and their types.
        Example descriptor: {"riskFactorID": "ust5Y_falling", "riskFactorType": "ReferenceIndex"}
        """
        payload = {
            "scenarioID": scenarioID,
            "riskFactorDescriptors": riskFactorDescriptors
        }

        response = requests.post(
            url=f"{self.serverURL}/addScenario",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        print(response)
        return response.status_code

    def find_all_scenarios(self):
        """
        Returns all defined scenarios.
        """
        response = requests.get(f"{self.serverURL}/findAllScenarios")
        response.raise_for_status()
        return response.json()
    
class PublicRiskService(RiskService):
    def __init__(self):
        super().__init__(
            serverURL="https://dadfir3-riskservice.zhaw.ch/"
        )





