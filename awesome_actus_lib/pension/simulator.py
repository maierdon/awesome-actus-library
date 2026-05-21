from copy import deepcopy
from datetime import date
from typing import List

from ..models.cashFlowStream import CashFlowStream
from . import events as ev
from .cohort import Cohort
from .fund import PensionFund


class ClosedFundSimulator:
    """Stage 1 simulator: closed fund, annual steps, no mortality, no new entries.

    Cohorts age year-by-year. Active cohorts accrue AGH from contributions
    and applied interest. At retirement_age the per-capita AGH converts to an
    annual pension via conversion_rate, then the cohort emits PENSION_PAYMENT
    events each year until terminal_age.

    Run produces an AAL CashFlowStream consumable by ValueAnalysis,
    IncomeAnalysis, LiquidityAnalysis.
    """

    def __init__(self, fund: PensionFund):
        self.fund = fund

    def run(self, horizon_years: int) -> CashFlowStream:
        per_contract_events = {c.cohort_id: [] for c in self.fund.cohorts}
        # Deep copy to keep input fund immutable across runs.
        cohorts = [deepcopy(c) for c in self.fund.cohorts]
        policy = self.fund.policy
        start = self.fund.start_date

        for year_offset in range(horizon_years):
            sim_year = start.year + year_offset
            event_date = date(sim_year, 12, 31).isoformat() + "T00:00:00"

            for cohort in cohorts:
                age = sim_year - cohort.birth_year
                if age >= policy.terminal_age:
                    continue
                self._step_cohort(
                    cohort=cohort,
                    age=age,
                    event_date=event_date,
                    sink=per_contract_events[cohort.cohort_id],
                    policy=policy,
                )

        raw_response = [
            {"contractID": cid, "events": evts, "children": []}
            for cid, evts in per_contract_events.items()
        ]
        return CashFlowStream(
            portfolio=self.fund.to_dummy_portfolio(),
            riskFactors=None,
            raw_response=raw_response,
        )

    def _step_cohort(self, cohort: Cohort, age: int, event_date: str, sink: list, policy):
        if cohort.status == "active":
            if age < policy.retirement_age:
                self._emit_active(cohort, age, event_date, sink, policy)
            else:
                self._emit_retirement(cohort, event_date, sink, policy)
        else:
            self._emit_pension(cohort, event_date, sink)

    def _emit_active(self, cohort: Cohort, age: int, event_date: str, sink: list, policy):
        insured = policy.insured_salary(cohort.gross_salary)
        sav_rate = policy.savings_rate(age)
        sav_amt = sav_rate * insured * cohort.headcount
        risk_amt = policy.risk_contribution_rate * insured * cohort.headcount
        admin = policy.admin_cost_per_member * cohort.headcount

        interest_pc = cohort.accrued_savings * policy.applied_interest_rate
        cohort.accrued_savings = cohort.accrued_savings + interest_pc + sav_rate * insured

        sink.append({"time": event_date, "type": ev.SAV_CONTRIB, "payoff": sav_amt})
        sink.append({"time": event_date, "type": ev.RISK_CONTRIB, "payoff": risk_amt})
        sink.append({"time": event_date, "type": ev.INTEREST_CREDIT,
                     "payoff": 0.0, "interest_per_capita": interest_pc})
        sink.append({"time": event_date, "type": ev.ADMIN_COST, "payoff": -admin})

    def _emit_retirement(self, cohort: Cohort, event_date: str, sink: list, policy):
        cohort.annual_pension = cohort.accrued_savings * policy.conversion_rate
        cohort.status = "retired"
        sink.append({
            "time": event_date,
            "type": ev.RETIREMENT_CONV,
            "payoff": 0.0,
            "agh_per_capita_at_conversion": cohort.accrued_savings,
            "annual_pension_per_capita": cohort.annual_pension,
        })
        self._emit_pension(cohort, event_date, sink)

    def _emit_pension(self, cohort: Cohort, event_date: str, sink: list):
        amount = -(cohort.annual_pension or 0.0) * cohort.headcount
        sink.append({"time": event_date, "type": ev.PENSION_PAYMENT, "payoff": amount})
