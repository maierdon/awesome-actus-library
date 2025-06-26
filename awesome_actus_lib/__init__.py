# /__init__.py

from .models.portfolio import Portfolio
from .utils.businessRuleValidator import BusinessRuleValidator
from .utils.utils import get_long_name_for_acronym
from .utils.actus_applicability_rules_grouped import APPLICABILITY_RULES
from .controller.Infrastructure import ActusService, PublicActusService, RiskService
from .models.cashFlowStream import CashFlowStream
from .models.RiskFactor import RiskFactor, ReferenceIndex, YieldCurve
from .analysis.income import IncomeAnalysis
from .analysis.liquidity import LiquidityAnalysis
from .analysis.value import ValueAnalysis
# This file is part of AwesomeActusLib_dev, an open-source library for financial contracts.
# It provides a set of tools for modeling, analyzing, and validating financial contracts
# based on the ACTUS standard.

# Load and expose all contract types
from .models.PAM_gen import PAM
from .models.ANN_gen import ANN
from .models.LAM_gen import LAM
from .models.OPTNS_gen import OPTNS
from .models.BCS_gen import BCS
from .models.CAPFL_gen import CAPFL
from .models.CSH_gen import CSH
from .models.CEC_gen import CEC
from .models.COM_gen import COM
from .models.LAX_gen import LAX
from .models.FXOUT_gen import FXOUT
from .models.FUTUR_gen import FUTUR
from .models.CEG_gen import CEG
from .models.NAM_gen import NAM
from .models.SWPPV_gen import SWPPV
from .models.STK_gen import STK
from .models.UMP_gen import UMP
from .models.SWAPS_gen import SWAPS
from .models.CLM_gen import CLM
# Add more here as needed or automate this if you're codegen'ing

CONTRACT_CLASS_REGISTRY = {
    "PAM": PAM,
    "ANN": ANN,
    # ...
}

__all__ = [
    "PAM",
    "ANN",
    "Portfolio",
    "BusinessRuleValidator",
    "get_long_name_for_acronym",
    "APPLICABILITY_RULES",
    "CONTRACT_CLASS_REGISTRY",
    "ActusService",
    "PublicActusService", 
    "RiskService",
    "CashFlowStream",
    "RiskFactor",
    "ReferenceIndex"
]
