from datetime import datetime


class ContractTerm:
    """Abstract Class for Contract Terms."""
    def __init__(self, termName, value):
        self.termName = termName
        self.value = value
    
    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.termName}' = {self.value!r}>"

    def __str__(self):
        return f"{self.termName}: {self.value}"

class ActusTerm(ContractTerm):
    """Base class for ACTUS-defined contract terms."""

class RiskFactorReferenceTerm(ActusTerm):
    """Base class for ACTUS terms that reference a Risk Factor."""
    
class UserDefinedTerm(ContractTerm):
    """Base class for user-defined terms (not used by ACTUS simulation)."""


class AccruedInterest(ActusTerm):
    """Represents the 'accruedInterest' contract term.
    
    Accrued interest as per SD. In case of NULL, this value will be recalculated using IPANX, IPCL and IPNR information. Can be used to represent irregular next IP payments.
    
**Acronym**: `IPAC`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'accruedInterest' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="accruedInterest", value=value)

class AmortizationDate(ActusTerm):
    """Represents the 'amortizationDate' contract term.
    
    This Date is used to calculate the annuity amounts for ANN and ANX NGX CT's. Needs only to be set in case where the contract balloon at MD and MD is less than AD.
    
**Acronym**: `AMD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'amortizationDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'amortizationDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="amortizationDate", value=value)

class ArrayCycleAnchorDateOfInterestPayment(ActusTerm):
    """Represents the 'arrayCycleAnchorDateOfInterestPayment' contract term.
    
    Same like IPANX but as array
    
**Acronym**: `ARIPANXi`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'arrayCycleAnchorDateOfInterestPayment' must be a valid ISO 8601 string")
        else:
            raise TypeError("'arrayCycleAnchorDateOfInterestPayment' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="arrayCycleAnchorDateOfInterestPayment", value=value)

class ArrayCycleAnchorDateOfPrincipalRedemption(ActusTerm):
    """Represents the 'arrayCycleAnchorDateOfPrincipalRedemption' contract term.
    
    Same like PRANX but as array
    
**Acronym**: `ARPRANXj`
    **Default**: ``"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'arrayCycleAnchorDateOfPrincipalRedemption' must be a valid ISO 8601 string")
        else:
            raise TypeError("'arrayCycleAnchorDateOfPrincipalRedemption' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="arrayCycleAnchorDateOfPrincipalRedemption", value=value)

class ArrayCycleAnchorDateOfRateReset(ActusTerm):
    """Represents the 'arrayCycleAnchorDateOfRateReset' contract term.
    
    Same like RRANX but as array
    
**Acronym**: `ARRRANX`
    **Default**: ``"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'arrayCycleAnchorDateOfRateReset' must be a valid ISO 8601 string")
        else:
            raise TypeError("'arrayCycleAnchorDateOfRateReset' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="arrayCycleAnchorDateOfRateReset", value=value)

class ArrayCycleOfInterestPayment(ActusTerm):
    """Represents the 'arrayCycleOfInterestPayment' contract term.
    
    Same like IPCL but as array
    
**Acronym**: `ARIPCLi`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'arrayCycleOfInterestPayment' must be one of str, got " + type(value).__name__)
        super().__init__(termName="arrayCycleOfInterestPayment", value=value)

class ArrayCycleOfPrincipalRedemption(ActusTerm):
    """Represents the 'arrayCycleOfPrincipalRedemption' contract term.
    
    Same like PRCL but as array
    
**Acronym**: `ARPRCLj`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'arrayCycleOfPrincipalRedemption' must be one of str, got " + type(value).__name__)
        super().__init__(termName="arrayCycleOfPrincipalRedemption", value=value)

class ArrayCycleOfRateReset(ActusTerm):
    """Represents the 'arrayCycleOfRateReset' contract term.
    
    Same like RRCL but as array
    
**Acronym**: `ARRRCL`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'arrayCycleOfRateReset' must be one of str, got " + type(value).__name__)
        super().__init__(termName="arrayCycleOfRateReset", value=value)

class ArrayFixedVariable(ActusTerm):
    """Represents the 'arrayFixedVariable' contract term.
    
    For array-type rate reset schedules, this attributes defines the meaning of ARRATE.
    
**Acronym**: `ARFIXVAR`
    **Default**: ``
    **Allowed Values:**
    - `fixedRate` (`F`): Rate spread represents a fixed rate.
    - `variableRate` (`V`): Rate spread represents the spread on top of a reference rate."""
    def __init__(self, value):
        if not isinstance(value, (list, str)):
            raise TypeError("'arrayFixedVariable' must be one of list, str, got " + type(value).__name__)
        super().__init__(termName="arrayFixedVariable", value=value)

class ArrayIncreaseDecrease(ActusTerm):
    """Represents the 'arrayIncreaseDecrease' contract term.
    
    Indicates whether a certain PRNXT element in ARPRNX increases the principal (NT) or decreases it.
Applies only for ANX, NAX, LAX Maturity CTs. For all other Maturity CTs the first principal payment is always in the opposite direction of all other (following) payments.
    
**Acronym**: `ARINCDEC`
    **Default**: ``
    **Allowed Values:**
    - `increase` (`INC`): Notional is increased in this period.
    - `decrease` (`DEC`): Notional is decreased in this period."""
    def __init__(self, value):
        if not isinstance(value, (list, str)):
            raise TypeError("'arrayIncreaseDecrease' must be one of list, str, got " + type(value).__name__)
        super().__init__(termName="arrayIncreaseDecrease", value=value)

class ArrayNextPrincipalRedemptionPayment(ActusTerm):
    """Represents the 'arrayNextPrincipalRedemptionPayment' contract term.
    
    Same like PRNXT but as array
    
**Acronym**: `ARPRNXTj`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (list, float, int)):
            raise TypeError("'arrayNextPrincipalRedemptionPayment' must be one of list, float, int, got " + type(value).__name__)
        super().__init__(termName="arrayNextPrincipalRedemptionPayment", value=value)

class ArrayRate(ActusTerm):
    """Represents the 'arrayRate' contract term.
    
    For array-type rate reset schedules, this attribute represents either an interest rate (corresponding to IPNR) or a spread (corresponding to RRSP). Which case applies depends on the attribute ARFIXVAR: if ARFIXVAR=FIX then it represents the new IPNR and if ARFIXVAR=VAR then the applicable RRSP.
    
**Acronym**: `ARRATE`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (list, float, int)):
            raise TypeError("'arrayRate' must be one of list, float, int, got " + type(value).__name__)
        super().__init__(termName="arrayRate", value=value)

class BoundaryCrossedFlag(ActusTerm):
    """Represents the 'boundaryCrossedFlag' contract term.
    
    Initializes the value of Boundary Crossed Flag state variable at statusDate
    
**Acronym**: `BCF`
    **Default**: `FALSE`"""
    def __init__(self, value):
        if not isinstance(value, (bool)):
            raise TypeError("'boundaryCrossedFlag' must be one of bool, got " + type(value).__name__)
        super().__init__(termName="boundaryCrossedFlag", value=value)

class BoundaryDirection(ActusTerm):
    """Represents the 'boundaryDirection' contract term.
    
    Boundary direction specifies the direction of motion in the underlying asset's price which will be considered a valid crossing of the boundary and trigger the boundary effect changing which, if any, of the boundary legs is  active.
    
**Acronym**: `BDR`
    **Default**: ``
    **Allowed Values:**
    - `fromBelow` (`INCR`): Boundary effect is trigerred if the observed underlying asset value is greater than or equal to the boundary value at a monitor time.
    - `fromAbove` (`DECR`): Boundary action if observed market object value less than or equal to boundary value at a monitor time."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'boundaryDirection' must be one of str, got " + type(value).__name__)
        super().__init__(termName="boundaryDirection", value=value)

class BoundaryEffect(ActusTerm):
    """Represents the 'boundaryEffect' contract term.
    
    This term specifies which leg - if any-  becomes the active subcontract  when the underlying asset's price crosses the specified boundary value in the specified direction triggerring a boundary crossing event.
    
**Acronym**: `BEF`
    **Default**: ``
    **Allowed Values:**
    - `knockINFirstLeg` (`INFIL`): effect of boundary crossing is to knock IN the first leg making this the active contract; monitoring of the boundary stops.
    - `knockINSecondLeg` (`INSEL`): effect of boundary crossing is to knock IN the Second Leg making this the active contract; monitoring of the boundary stops.
    - `knockOUTCurrentLeg` (`OUT`): effect of boundary crossing is to knockOUT any active contract so there is no active contract after the boundary crossing; monitoring of the boundary stops."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'boundaryEffect' must be one of str, got " + type(value).__name__)
        super().__init__(termName="boundaryEffect", value=value)

class BoundaryLegInitiallyActive(ActusTerm):
    """Represents the 'boundaryLegInitiallyActive' contract term.
    
    Specifies which leg - if any - is the active contract  in effect when the boundary controlled switch contract starts.
    
**Acronym**: `BLIA`
    **Default**: `there is no active subcontract`
    **Allowed Values:**
    - `firstLeg` (`FIL`): the first leg is active when the boundary controlled switch contract is initialized.
    - `secondLeg` (`SEL`): the second leg is active when the boundary controlled switch contract starts.
    - `Null` (`Null`): there is no active subcontract when the boundary controlled switch contract starts."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'boundaryLegInitiallyActive' must be one of str, got " + type(value).__name__)
        super().__init__(termName="boundaryLegInitiallyActive", value=value)

class BoundaryMonitoringAnchorDate(ActusTerm):
    """Represents the 'boundaryMonitoringAnchorDate' contract term.
    
    The first Boundary monitoring event occurs on this date
    
**Acronym**: `BMANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'boundaryMonitoringAnchorDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'boundaryMonitoringAnchorDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="boundaryMonitoringAnchorDate", value=value)

class BoundaryMonitoringCycle(ActusTerm):
    """Represents the 'boundaryMonitoringCycle' contract term.
    
    The frequency with which boundary monitoring events occur. It defines how often the system checks to test whether the  market value of the underlying asset has crossed the boundary in the specified direction triggerring  a boundary crossing event.
    
**Acronym**: `BMCL`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'boundaryMonitoringCycle' must be one of str, got " + type(value).__name__)
        super().__init__(termName="boundaryMonitoringCycle", value=value)

class BoundaryMonitoringEndDate(ActusTerm):
    """Represents the 'boundaryMonitoringEndDate' contract term.
    
    Boundary monitoring ends on this date
    
**Acronym**: `BMED`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'boundaryMonitoringEndDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'boundaryMonitoringEndDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="boundaryMonitoringEndDate", value=value)

class BoundaryValue(ActusTerm):
    """Represents the 'boundaryValue' contract term.
    
    Boundary value in a barrier options contract, when reached, triggers the boundary effect specified e.g. Knock-In or Knock-out
    
**Acronym**: `BV`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'boundaryValue' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="boundaryValue", value=value)

class BusinessDayConvention(ActusTerm):
    """Represents the 'businessDayConvention' contract term.
    
    BDC's are linked to a calendar. Calendars have working and non-working days. A BDC value other than N means that cash flows cannot fall on non-working days, they must be shifted to the next business day (following) or the previous on (preceding).
These two simple rules get refined twofold:
- Following modified (preceding): Same like following (preceding), however if a cash flow gets shifted into a new month, then  it is shifted to preceding (following) business day.
- Shift/calculate (SC) and calculate/shift (CS). Accrual, principal, and possibly other calculations are affected by this choice. In the case of SC first the dates are shifted and after the shift cash flows are calculated. In the case of CS it is the other way round.
Attention: Does not affect non-cyclical dates such as PRD, MD, TD, IPCED since they can be set to the correct date directly.
    
**Acronym**: `BDC`
    **Default**: `nos`
    **Allowed Values:**
    - `noShift` (`NOS`): No shift applied to non-business days.
    - `shiftCalculateFollowing` (`SCF`): Shift event dates first then calculate accruals etc. Strictly shift to the next following business day.
    - `shiftCalculateModifiedFollowing` (`SCMF`): Shift event dates first then calculate accruals etc. Shift to the next following business day if this falls in the same month. Shift to the most recent preceding business day otherwise.
    - `calculateShiftFollowing` (`CSF`): Calculate accruals etc. first then shift event dates. Strictly shift to the next following business day.
    - `calculateShiftModifiedFollowing` (`CSMF`): Calculate accruals etc. first then shift event dates. Shift to the next following business day if this falls in the same month. Shift to the most recent preceding business day otherwise.
    - `shiftCalculatePreceding` (`SCP`): Shift event dates first then calculate accruals etc. Strictly shift to the most recent preceding business day.
    - `shiftCalculateModifiedPreceding` (`SCMP`): Shift event dates first then calculate accruals etc. Shift to the most recent preceding business day if this falls in the same month. Shift to the next following business day otherwise.
    - `calculateShiftPreceding` (`CSP`): Calculate accruals etc. first then shift event dates. Strictly shift to the most recent preceding business day.
    - `calculateShiftModifiedPreceding` (`SCMP`): Calculate accruals etc. first then shift event dates. Shift to the most recent preceding business day if this falls in the same month. Shift to the next following business day otherwise."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'businessDayConvention' must be one of str, got " + type(value).__name__)
        super().__init__(termName="businessDayConvention", value=value)

class Calendar(ActusTerm):
    """Represents the 'calendar' contract term.
    
    Calendar defines the non-working days which affect the dates of contract events (CDE's) in combination with EOMC and BDC. Custom calendars can be added as additional enum options.
    
**Acronym**: `CLDR`
    **Default**: `noCalendar`
    **Allowed Values:**
    - `noCalendar` (`NC`): No holidays defined
    - `mondayToFriday` (`MF`): Saturdays and Sundays are holidays"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'calendar' must be one of str, got " + type(value).__name__)
        super().__init__(termName="calendar", value=value)

class CapitalizationEndDate(ActusTerm):
    """Represents the 'capitalizationEndDate' contract term.
    
    If IPCED is set, then interest is not paid or received but added to the balance (NT) until IPCED. If IPCED does not coincide with an IP cycle, one additional interest payment gets calculated at IPCED and capitalized. Thereafter normal interest payments occur.
    
**Acronym**: `IPCED`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'capitalizationEndDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'capitalizationEndDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="capitalizationEndDate", value=value)

class ClearingHouse(ActusTerm):
    """Represents the 'clearingHouse' contract term.
    
    Indicates wheter CRID takes a clearing house function or not. In other word, whether CRID receive margins (MRIM, MRVM).
    
**Acronym**: `MRCLH`
    **Default**: ``
    **Allowed Values:**
    - `isClearingHouse` (`Y`): Contract creator is the clearing house.
    - `isNotClearingHouse` (`N`): Contract creator is not the clearing house."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'clearingHouse' must be one of str, got " + type(value).__name__)
        super().__init__(termName="clearingHouse", value=value)

class ContractDealDate(ActusTerm):
    """Represents the 'contractDealDate' contract term.
    
    This date signifies the origination of the contract where an agreement between the customer and the bank has been settled. From this date on, the institution will have a (market) risk position for financial contracts. This is even the case when IED is in future.
    
**Acronym**: `CDD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'contractDealDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'contractDealDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="contractDealDate", value=value)

class ContractID(ActusTerm):
    """Represents the 'contractID' contract term.
    
    Unique identifier of a contract.  
If the system is used on a single firm level, an internal unique ID can be generated. If used on a national or globally level, a globally unique ID is required.
    
**Acronym**: `CID`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'contractID' must be one of str, got " + type(value).__name__)
        super().__init__(termName="contractID", value=value)

class ContractPerformance(ActusTerm):
    """Represents the 'contractPerformance' contract term.
    
    Indicates the current contract performance status. Different states of the contract range from performing to default.
    
**Acronym**: `PRF`
    **Default**: `PF`
    **Allowed Values:**
    - `performant` (`PF`): Contract is performing according to terms and conditions.
    - `delayed` (`DL`): Contractual payment obligations are delayed according to the Grace Period.
    - `delinquent` (`DQ`): Contractual payment obligations are delinquent according to the Delinquency Period.
    - `default` (`DF`): Contract defaulted on payment obligations according to Delinquency Period.
    - `matured` (`MA`): Contract matured.
    - `terminated` (`TE`): Contract has been terminated."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'contractPerformance' must be one of str, got " + type(value).__name__)
        super().__init__(termName="contractPerformance", value=value)

class ContractRole(ActusTerm):
    """Represents the 'contractRole' contract term.
    
    CNTRL defines which position the CRID ( the creator of the contract record ) takes in a contract. For example, whether the contract is an asset or liability, a long or short position for the CRID. 
Most contracts are simple on or off balance sheet positions which are assets, liabilities. Such contracts can also play a secondary role as a collateral. 
The attribute is highly significant since it determines the direction of all cash flows. The exact meaning is given with each CT in the ACTUS High Level Specification document.
    
**Acronym**: `CNTRL`
    **Default**: ``
    **Allowed Values:**
    - `realPositionAsset` (`RPA`): Contract creator takes the asset or lender side.
    - `realPositionLiability` (`RPL`): Contract creator takes the liability or borrower side.
    - `receiveFirstLegl` (`RFL`): Contract creator receives the first leg.
    - `payFirstLeg` (`PFL`): Contract creator pays the first leg.
    - `receiveFix` (`RF`): Contract creator receives the fixed leg.
    - `payFix` (`PF`): Contract creator pays the fixed leg.
    - `buyer` (`BUY`): Contract creator holds the right to buy the underlying / exercise the option.
    - `seller` (`SEL`): Contract creator holds the obligation to sell the underlying / deliver the option.
    - `collateralPosition` (`COL`): Contract represents a collateral to an underlying instrument
    - `closeOutNetting` (`CNO`): Contract creator and counterparty agree on netting payment obligations of underlying instruments in case of default.
    - `underlying` (`UDL`): Contract represents the underlying to a composed contract. Role of the underlying is derived from the parent.
    - `underlyingPlus` (`UDLP`): Contract represents the underlying to a composed contract. Role of the underlying is derived from the parent. When considered a standalone contract the underlying’s creator takes the asset side.
    - `underlyingMinus` (`UDLM`): Contract represents the underlying to a composed contract. Role of the underlying is derived from the parent. When considered a standalone contract the underlying’s creator takes the liability side."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'contractRole' must be one of str, got " + type(value).__name__)
        super().__init__(termName="contractRole", value=value)

class ContractStructure(ActusTerm):
    """Represents the 'contractStructure' contract term.
    
    A structure identifying individual or sets of underlying contracts. E.g. for FUTUR, this structure identifies the single underlying contract, for SWAPS, the FirstLeg and SecondLeg are identified, or for CEG, CEC the structure identifies Covered and Covering contracts.
    
**Acronym**: `CTS`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (list, str)):
            raise TypeError("'contractStructure' must be one of list, str, got " + type(value).__name__)
        super().__init__(termName="contractStructure", value=value)

class ContractType(ActusTerm):
    """Represents the 'contractType' contract term.
    
    The ContractType is the most important information. It defines the cash flow generating pattern of a contract. The ContractType information in combination with a given state of the risk factors will produce a deterministic sequence of cash flows which are the basis of any financial analysis.
    
**Acronym**: `CT`
    **Default**: ``
    **Allowed Values:**
    - `principalAtMaturity` (`PAM`): Lending agreements with full amortization at maturity.
    - `annuity` (`ANN`): Lending agreements with fixed periodic payments consisting of an interest and principal portion. The periodic payments are adjusted for variable rate instruments such that maturity remains fixed.
    - `negativeAmortizer` (`NAM`): Lending agreements with fixed periodic payments consisting of an interest and principal portion. Maturity changes for variable rate instruments.
    - `linearAmortizer` (`LAM`): Lending agreements with fixed principal repayment amounts and variable interest payments.
    - `exoticLinearAmortizer` (`LAX`): Lending agreements with exotic repayment schedules.
    - `callMoney` (`CLM`): Lonas that are rolled over as long as they are not called. Once called it has to be paid back after the stipulated notice period.
    - `undefinedMaturityProfile` (`UMP`): Interest paying cash accounts (current / savings / etc.).
    - `cash` (`CSH`): Represents cash holdings.
    - `stock` (`STK`): Represents stocks/shares/equity.
    - `commodity` (`COM`): Represents commodities.
    - `swap` (`SWAPS`): An agreement of swapping two legs such as fixed against variable or currency 1 against currency 2 etc.
    - `plainVanillaSwap` (`SWPPV`): Plain vanilla interest rate swaps.
    - `foreignExchangeOutright` (`FXOUT`): An agreement of swapping two cash flows in different currencies at a future point in time.
    - `capFloor` (`CAPFL`): An agreement of paying the differential (cap or floor) of a reference rate versus a fixed rate.
    - `future` (`FUTUR`): An agreement of exchanging an underlying instrument against a fixed price in the future.
    - `option` (`OPTNS`): Different types of options on buying an underlying instrument at a fixed price in the future.
    - `creditEnhancementGuarantee` (`CEG`): A guarantee / letter of credit by a third party on the scheduled payment obligations of an underlying instrument
    - `creditEnhancementCollateral` (`CEC`): A collateral securing the scheduled payment obligations of an underlying instrument"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'contractType' must be one of str, got " + type(value).__name__)
        super().__init__(termName="contractType", value=value)

class CounterpartyID(ActusTerm):
    """Represents the 'counterpartyID' contract term.
    
    CPID identifies the counterparty to the CRID in this contract.
CPID is ideally the official LEI which can be a firm, a government body, even a single person etc. However, this can also refer to a annonymous group in which case this information is not to be disclosed. CPID may also refer to a group taking a joint risk or more generally, CPID is the main counterparty, against which the contract has been settled.
    
**Acronym**: `CPID`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'counterpartyID' must be one of str, got " + type(value).__name__)
        super().__init__(termName="counterpartyID", value=value)

class CoverageOfCreditEnhancement(ActusTerm):
    """Represents the 'coverageOfCreditEnhancement' contract term.
    
    Defines which percentage of the exposure is covered
    
**Acronym**: `CECV`
    **Default**: `1`
    **Allowed Values:**
    - `(0,1)`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'coverageOfCreditEnhancement' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="coverageOfCreditEnhancement", value=value)

class CreatorID(ActusTerm):
    """Represents the 'creatorID' contract term.
    
    This identifies the legal entity creating the contract record. The counterparty of the contract is tracked in CPID.
CRID is ideally the official LEI which can be a firm, a government body, even a single person etc. However, this can also refer to a annonymous group in which case this information is not to be disclosed. CRID may also refer to a group taking a joint risk.
    
**Acronym**: `CRID`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'creatorID' must be one of str, got " + type(value).__name__)
        super().__init__(termName="creatorID", value=value)

class CreditEventTypeCovered(ActusTerm):
    """Represents the 'creditEventTypeCovered' contract term.
    
    The type of credit events covered e.g. in credit enhancement or credit default swap contracts. Only the defined credit event types may trigger the protection.
    
**Acronym**: `CETC`
    **Default**: `DF`
    **Allowed Values:**
    - `delayed` (`DL`): Delay of the underlying represents a credit event.
    - `delinquent` (`DQ`): Delinquency of the underlying represents a credit event.
    - `default` (`DF`): Default of the underlying represents a credit event."""
    def __init__(self, value):
        if not isinstance(value, (list, str)):
            raise TypeError("'creditEventTypeCovered' must be one of list, str, got " + type(value).__name__)
        super().__init__(termName="creditEventTypeCovered", value=value)

class CreditLineAmount(ActusTerm):
    """Represents the 'creditLineAmount' contract term.
    
    If defined, gives the total amount that can be drawn from a credit line. The remaining amount that can still be drawn is given by CLA-NT.
For ANN, NAM, the credit line can only be drawn prior to PRANX-1PRCL.
For CRL, the remaining amount that can still be drawn is given by CLA-Sum(NT of attached contracts).
    
**Acronym**: `CLA`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'creditLineAmount' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="creditLineAmount", value=value)

class Currency(ActusTerm):
    """Represents the 'currency' contract term.
    
    The currency of the cash flows.
    
**Acronym**: `CUR`
    **Default**: ``
    **Allowed Values:**
    - `ISO4217`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'currency' must be one of str, got " + type(value).__name__)
        super().__init__(termName="currency", value=value)

class Currency2(ActusTerm):
    """Represents the 'currency2' contract term.
    
    The currency of the cash flows of the second leg (if not defined, main currency applies)
    
**Acronym**: `CUR2`
    **Default**: ``
    **Allowed Values:**
    - `ISO4217`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'currency2' must be one of str, got " + type(value).__name__)
        super().__init__(termName="currency2", value=value)

class CycleAnchorDateOfDividend(ActusTerm):
    """Represents the 'cycleAnchorDateOfDividend' contract term.
    
    Date from which the dividend payment date schedule is calculated according to the cycle length. The first dividend payment event takes place on this anchor.
    
**Acronym**: `DVANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfDividend' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfDividend' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfDividend", value=value)

class CycleAnchorDateOfFee(ActusTerm):
    """Represents the 'cycleAnchorDateOfFee' contract term.
    
    Date from which the fee payment date schedule is calculated according to the cycle length. The first fee payment event takes place on this anchor.
    
**Acronym**: `FEANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfFee' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfFee' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfFee", value=value)

class CycleAnchorDateOfInterestCalculationBase(ActusTerm):
    """Represents the 'cycleAnchorDateOfInterestCalculationBase' contract term.
    
    Date from which the interest calculation base date schedule is calculated according to the cycle length. The first interest calculation base event takes place on this anchor.
    
**Acronym**: `IPCBANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfInterestCalculationBase' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfInterestCalculationBase' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfInterestCalculationBase", value=value)

class CycleAnchorDateOfInterestPayment(ActusTerm):
    """Represents the 'cycleAnchorDateOfInterestPayment' contract term.
    
    Date from which the interest payment date schedule is calculated according to the cycle length. The first interest payment event takes place on this anchor.
    
**Acronym**: `IPANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfInterestPayment' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfInterestPayment' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfInterestPayment", value=value)

class CycleAnchorDateOfMargining(ActusTerm):
    """Represents the 'cycleAnchorDateOfMargining' contract term.
    
    Date from which the margin call date schedule is calculated according to the cycle length. The first margin call event takes place on this anchor.
    
**Acronym**: `MRANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfMargining' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfMargining' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfMargining", value=value)

class CycleAnchorDateOfOptionality(ActusTerm):
    """Represents the 'cycleAnchorDateOfOptionality' contract term.
    
    Used for Basic Maturities (such as PAM, RGM, ANN, NGM and their Step-up versions) and American and Bermudan style options. 
- Basic Maturities: Within the group of these Maturities, it indicates the possibility of prepayments. Prepayment features are controlled by Behavior. 
- American and Bermudan style Options: Begin of exercise period.
    
**Acronym**: `OPANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfOptionality' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfOptionality' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfOptionality", value=value)

class CycleAnchorDateOfPrincipalRedemption(ActusTerm):
    """Represents the 'cycleAnchorDateOfPrincipalRedemption' contract term.
    
    Date from which the principal payment date schedule is calculated according to the cycle length. The first principal payment event takes place on this anchor.
    
**Acronym**: `PRANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfPrincipalRedemption' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfPrincipalRedemption' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfPrincipalRedemption", value=value)

class CycleAnchorDateOfRateReset(ActusTerm):
    """Represents the 'cycleAnchorDateOfRateReset' contract term.
    
    Date from which the rate reset date schedule is calculated according to the cycle length. The first rate reset event takes place on this anchor.
    
**Acronym**: `RRANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfRateReset' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfRateReset' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfRateReset", value=value)

class CycleAnchorDateOfScalingIndex(ActusTerm):
    """Represents the 'cycleAnchorDateOfScalingIndex' contract term.
    
    Date from which the scaling date schedule is calculated according to the cycle length. The first scaling event takes place on this anchor.
    
**Acronym**: `SCANX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'cycleAnchorDateOfScalingIndex' must be a valid ISO 8601 string")
        else:
            raise TypeError("'cycleAnchorDateOfScalingIndex' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="cycleAnchorDateOfScalingIndex", value=value)

class CycleOfDividend(ActusTerm):
    """Represents the 'cycleOfDividend' contract term.
    
    Defines in combination with DVANX the payment points of dividends. The dividend payment schedule will start at DVANX and end at MaximumProjectionPeriod (cf. sheet Modeling Parameters).
    
**Acronym**: `DVCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfDividend' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfDividend", value=value)

class CycleOfFee(ActusTerm):
    """Represents the 'cycleOfFee' contract term.
    
    Defines in combination with FEANX the payment points of fees
    
**Acronym**: `FECL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfFee' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfFee", value=value)

class CycleOfInterestCalculationBase(ActusTerm):
    """Represents the 'cycleOfInterestCalculationBase' contract term.
    
    Concerning the format see PRCL. 
Defines the subsequent adjustment points to NT of the interest payment calculation base.
    
**Acronym**: `IPCBCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfInterestCalculationBase' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfInterestCalculationBase", value=value)

class CycleOfInterestPayment(ActusTerm):
    """Represents the 'cycleOfInterestPayment' contract term.
    
    Cycle according to which the interest payment date schedule will be calculated.
In case IPCL is not set, then there will only be an interest payment event at MD (and possibly at IPANX if set).
The interval will be adjusted yet by EOMC and BDC.
    
**Acronym**: `IPCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfInterestPayment' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfInterestPayment", value=value)

class CycleOfMargining(ActusTerm):
    """Represents the 'cycleOfMargining' contract term.
    
    Defines together with MRANX the points where margins can be called.
    
**Acronym**: `MRCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfMargining' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfMargining", value=value)

class CycleOfOptionality(ActusTerm):
    """Represents the 'cycleOfOptionality' contract term.
    
    Cycle according to which the option exercise date schedule will be calculated.
OPCL can be NULL for American Options or Prepayment Optionality in which case the optionality period starts at OPANX and ends at OPXED (for american options) or MD (in case of prepayment optionality).
The interval will be adjusted yet by EOMC and BDC.
    
**Acronym**: `OPCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfOptionality' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfOptionality", value=value)

class CycleOfPrincipalRedemption(ActusTerm):
    """Represents the 'cycleOfPrincipalRedemption' contract term.
    
    Cycle according to which the interest payment date schedule will be calculated.
In case PRCL is not set, then there will only be one principal payment event at MD (and possibly at PRANX if set).
The interval will be adjusted yet by EOMC and BDC.
    
**Acronym**: `PRCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfPrincipalRedemption' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfPrincipalRedemption", value=value)

class CycleOfRateReset(ActusTerm):
    """Represents the 'cycleOfRateReset' contract term.
    
    Cycle according to which the rate reset date schedule will be calculated.
In case RRCL is not set, then there will only be one rate reset event at RRANX given RRANX if set.
The interval will be adjusted yet by EOMC and BDC.
    
**Acronym**: `RRCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfRateReset' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfRateReset", value=value)

class CycleOfScalingIndex(ActusTerm):
    """Represents the 'cycleOfScalingIndex' contract term.
    
    Cycle according to which the scaling date schedule will be calculated.
In case SCCL is not set, then there will only be one scaling event at SCANX given SCANX is set.
The interval will be adjusted yet by EOMC and BDC.
    
**Acronym**: `SCCL`
    **Default**: ``
    **Allowed Values:**
    - `[ISO8601 Duration]L[s={0,1}]`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cycleOfScalingIndex' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cycleOfScalingIndex", value=value)

class CyclePointOfInterestPayment(ActusTerm):
    """Represents the 'cyclePointOfInterestPayment' contract term.
    
    Usually, interest is paid at the end of each IPCL which corresponds to a IPPNT value of E which is also the default. If interest payment occurs at the beginning of the cycle, the value is B.
    
**Acronym**: `IPPNT`
    **Default**: `E`
    **Allowed Values:**
    - `beginning` (`B`): Interest is paid upfront of the interest period.
    - `end` (`E`): Interest is paid at the end of the interest period."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cyclePointOfInterestPayment' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cyclePointOfInterestPayment", value=value)

class CyclePointOfRateReset(ActusTerm):
    """Represents the 'cyclePointOfRateReset' contract term.
    
    Normally rates get reset at the beginning of any resetting cycles. There are contracts where the rate is not set at the beginning but at the end of the cycle and then applied to the previous cycle (post-fixing); in other words the rate applies before it is fixed. Hence, the new rate is not known during the entire cycle where it applies. Therefore, the rate will be applied backwards at the end of the cycle. This happens through a correction of interest accrued.
    
**Acronym**: `RRPNT`
    **Default**: `B`
    **Allowed Values:**
    - `beginning` (`B`): The new rate is applied at the beginning of the reset period.
    - `end` (`E`): The new rate is applied at the end of the reset period."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'cyclePointOfRateReset' must be one of str, got " + type(value).__name__)
        super().__init__(termName="cyclePointOfRateReset", value=value)

class DayCountConvention(ActusTerm):
    """Represents the 'dayCountConvention' contract term.
    
    Method defining how days are counted between two dates. This finally defines the year fraction in accrual calculations.
    
**Acronym**: `IPDC`
    **Default**: ``
    **Allowed Values:**
    - `actualActual` (`AA`): Year fractions accrue on the basis of the actual number of days per month and per year in the respective period.
    - `actualThreeSixty` (`A360`): Year fractions accrue on the basis of the actual number of days per month and 360 days per year in the respective period.
    - `actualThreeSixtyFive` (`A365`): Year fractions accrue on the basis of the actual number of days per month and 365 days per year in the respective period.
    - `thirtyEThreeSixtyISDA` (`30E360ISDA`): Year fractions accrue on the basis of 30 days per month and 360 days per year in the respective period (ISDA method).
    - `thirtyEThreeSixty` (`30E360`): Year fractions accrue on the basis of 30 days per month and 360 days per year in the respective period.
    - `twentyEightEThreeThirtySix` (`28E336`): Year fractions accrue on the basis of 28 days per month and 336 days per year in the respective period."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'dayCountConvention' must be one of str, got " + type(value).__name__)
        super().__init__(termName="dayCountConvention", value=value)

class DelinquencyPeriod(ActusTerm):
    """Represents the 'delinquencyPeriod' contract term.
    
    If real payment happens after scheduled payment date plus DLP, then the counterparty is in technical default. This means that the creditor legally has the right to declare default of the debtor.
    
**Acronym**: `DQP`
    **Default**: `P0D`
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'delinquencyPeriod' must be one of str, got " + type(value).__name__)
        super().__init__(termName="delinquencyPeriod", value=value)

class DelinquencyRate(ActusTerm):
    """Represents the 'delinquencyRate' contract term.
    
    Rate at which Delinquency Payments accrue on NT (in addition to the interest rate) during the DelinquencyPeriod
    
**Acronym**: `DQR`
    **Default**: `0`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'delinquencyRate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="delinquencyRate", value=value)

class DeliverySettlement(ActusTerm):
    """Represents the 'deliverySettlement' contract term.
    
    Indicates whether the contract is settled in cash or physical delivery.
In case of physical delivery, the underlying contract and associated (future) cash flows are effectively exchanged. In case of cash settlement, the current market value of the underlying contract determines the cash flow exchanged.
    
**Acronym**: `DS`
    **Default**: `D`
    **Allowed Values:**
    - `cashSettlement` (`S`): The market value of the underlying is settled.
    - `physicalSettlement` (`D`): The underlying is delivered physically."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'deliverySettlement' must be one of str, got " + type(value).__name__)
        super().__init__(termName="deliverySettlement", value=value)

class EndOfMonthConvention(ActusTerm):
    """Represents the 'endOfMonthConvention' contract term.
    
    When computing schedules a special problem arises if an anchor date is at the end of a month and a cycle of monthly or quarterly is applied (yearly in the case of leap years only). How do we have to interpret an anchor date April 30 plus 1M cycles? In case where EOM is selected, it will jump to the 31st of May, then June 30, July 31 and so on. If SM is selected, it will jump to the 30st always with of course an exception in February. 
This logic applies for all months having 30 or less days and an anchor date at the last day. Month with 31 days will at any rate jump to the last of the month if anchor date is on the last day.
    
**Acronym**: `EOMC`
    **Default**: `sd`
    **Allowed Values:**
    - `sameDay` (`SD`): Schedule times always fall on the schedule anchor date day of the month.
    - `endOfMonth` (`EOM`): Schedule times fall on the end of every month if the anchor date represents the last day of the respective month."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'endOfMonthConvention' must be one of str, got " + type(value).__name__)
        super().__init__(termName="endOfMonthConvention", value=value)

class ExDividendDate(ActusTerm):
    """Represents the 'exDividendDate' contract term.
    
    In case contract is traded between DVEX and next DV payment date (i.e. PRD>DVEX & PRD<next DV payment date), then the old holder of the contract (previous to the trade) receives the next DV payment. In other words, the next DV payment is cancelled for the new (after the trade) holder of the contract.
    
**Acronym**: `DVEX`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'exDividendDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'exDividendDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="exDividendDate", value=value)

class ExerciseAmount(ActusTerm):
    """Represents the 'exerciseAmount' contract term.
    
    The amount fixed at Exercise Date for a contingent event/obligation such as a forward condition, optionality etc. The Exercise Amount is fixed at Exercise Date but not settled yet.
    
**Acronym**: `XA`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'exerciseAmount' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="exerciseAmount", value=value)

class ExerciseDate(ActusTerm):
    """Represents the 'exerciseDate' contract term.
    
    Date of exercising a contingent event/obligation such as a forward condition, optionality etc. The Exercise date marks the observed timestamp of fixing the contingent event and respective payment obligation not necessarily the timestamp of settling the obligation.
    
**Acronym**: `XD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'exerciseDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'exerciseDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="exerciseDate", value=value)

class FeeAccrued(ActusTerm):
    """Represents the 'feeAccrued' contract term.
    
    Accrued fees as per SD
    
**Acronym**: `FEAC`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'feeAccrued' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="feeAccrued", value=value)

class FeeBasis(ActusTerm):
    """Represents the 'feeBasis' contract term.
    
    Basis, on which Fee is calculated. For FEB=’A’, FER is interpreted as an absolute amount to be paid at every FP event and for FEB=’N’, FER represents a rate at which FP amounts accrue on the basis of the contract’s NT.
    
**Acronym**: `FEB`
    **Default**: ``
    **Allowed Values:**
    - `absoluteValue` (`A`): The fee rate represents an absolute value.
    - `nonimalValueOfTheUnderlying` (`N`): The fee rate represents a rate that accrues fees on the basis of the nominal value of the underlying."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'feeBasis' must be one of str, got " + type(value).__name__)
        super().__init__(termName="feeBasis", value=value)

class FeeRate(ActusTerm):
    """Represents the 'feeRate' contract term.
    
    Rate of Fee which is a percentage of the underlying or FER is an absolute amount. For all contracts where FEB does not apply (cf. business rules), FER is interpreted as an absolute amount.
    
**Acronym**: `FER`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'feeRate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="feeRate", value=value)

class FixingPeriod(ActusTerm):
    """Represents the 'fixingPeriod' contract term.
    
    Interest rate resets (adjustments) are usually fixed one or two days (usually Business Days) before the new rate applies (defined by the rate reset schedule). This field holds the period between fixing and application of a rate.
    
**Acronym**: `RRFIX`
    **Default**: `P0D`
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'fixingPeriod' must be one of str, got " + type(value).__name__)
        super().__init__(termName="fixingPeriod", value=value)

class FuturesPrice(ActusTerm):
    """Represents the 'futuresPrice' contract term.
    
    The price the counterparties agreed upon at which the underlying contract (of a FUTUR) is exchanged/settled at STD. Quoting is different for different types of underlyings: Fixed Income = in percentage, all others in nominal terms.
    
**Acronym**: `PFUT`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'futuresPrice' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="futuresPrice", value=value)

class GracePeriod(ActusTerm):
    """Represents the 'gracePeriod' contract term.
    
    If real payment happens after scheduled payment date plus GRP, then the payment is in delay.
    
**Acronym**: `GRP`
    **Default**: `P0D`
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'gracePeriod' must be one of str, got " + type(value).__name__)
        super().__init__(termName="gracePeriod", value=value)

class GuaranteedExposure(ActusTerm):
    """Represents the 'guaranteedExposure' contract term.
    
    Defines which value of the exposure is covered:
- NO: Nominal Value
- NI: Nominal plus Interest
- MV: Market Value
    
**Acronym**: `CEGE`
    **Default**: ``
    **Allowed Values:**
    - `nominalValue` (`NO`): Nominal value of the exposure is covered.
    - `nominalValuePlusInterest` (`NI`): Nominal value of the exposure plus interest accrued is covered.
    - `marketValue` (`MV`): Market value of the exposure is covered."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'guaranteedExposure' must be one of str, got " + type(value).__name__)
        super().__init__(termName="guaranteedExposure", value=value)

class InitialExchangeDate(ActusTerm):
    """Represents the 'initialExchangeDate' contract term.
    
    Date of the initial cash flow for Maturity and Non-Maturity CT's. It also coincides with the beginning of interest accrual calculation.
    
**Acronym**: `IED`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'initialExchangeDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'initialExchangeDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="initialExchangeDate", value=value)

class InitialMargin(ActusTerm):
    """Represents the 'initialMargin' contract term.
    
    Margin to cover losses which may be incurred as a result of market fluctuations. 
Upon contract closing or maturity, the MRIM is reimbursed.
    
**Acronym**: `MRIM`
    **Default**: `0`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'initialMargin' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="initialMargin", value=value)

class InterestCalculationBase(ActusTerm):
    """Represents the 'interestCalculationBase' contract term.
    
    This is important for amortizing instruments. The basis of interest calculation is normally the notional outstanding amount as per SD. This is considered the fair basis and in many countries the only legal basis. If NULL or NTSD is selected, this is the case. 
Alternative bases (normally in order to favor the lending institution) are found. In the extreme case the original balance (PCDD=NT+PDCDD) never gets adjusted. In this case PCDD must be chosen. 
An intermediate case exist wherre balances do get adjusted, however with lags. In this case NTL mut be selected and anchor dates and cycles must be set.
    
**Acronym**: `IPCB`
    **Default**: `NT`
    **Allowed Values:**
    - `notioalOutstanding` (`NT`): Interest accrues on the basis of the notional outstanding.
    - `notionalAtInitialExchange` (`NTIED`): Interest accrues on the basis of the notional value at initial exchange.
    - `notionalLagged` (`NTL`): Interest accrues on the basis of the lagged notional outstanding."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'interestCalculationBase' must be one of str, got " + type(value).__name__)
        super().__init__(termName="interestCalculationBase", value=value)

class InterestCalculationBaseAmount(ActusTerm):
    """Represents the 'interestCalculationBaseAmount' contract term.
    
    This is the amount used for the calculation of interest. Calculation base per SD.
    
**Acronym**: `IPCBA`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'interestCalculationBaseAmount' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="interestCalculationBaseAmount", value=value)

class InterestScalingMultiplier(ActusTerm):
    """Represents the 'interestScalingMultiplier' contract term.
    
    The multiplier being applied to interest cash flows
    
**Acronym**: `SCIP`
    **Default**: `1`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'interestScalingMultiplier' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="interestScalingMultiplier", value=value)

class LifeCap(ActusTerm):
    """Represents the 'lifeCap' contract term.
    
    For variable rate basic CTs this represents a cap on the interest rate that applies during the entire lifetime of the contract.
For CAPFL CTs this represents the cap strike rate.
    
**Acronym**: `RRLC`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'lifeCap' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="lifeCap", value=value)

class LifeFloor(ActusTerm):
    """Represents the 'lifeFloor' contract term.
    
    For variable rate basic CTs this represents a floor on the interest rate that applies during the entire lifetime of the contract.
For CAPFL CTs this represents the floor strike rate.
    
**Acronym**: `RRLF`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'lifeFloor' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="lifeFloor", value=value)

class MaintenanceMarginLowerBound(ActusTerm):
    """Represents the 'maintenanceMarginLowerBound' contract term.
    
    Defines the lower bound of the Maintenance Margin. If MRVM falls below MRMML, then capital must be added to reach the original MRIM.
    
**Acronym**: `MRMML`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'maintenanceMarginLowerBound' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="maintenanceMarginLowerBound", value=value)

class MaintenanceMarginUpperBound(ActusTerm):
    """Represents the 'maintenanceMarginUpperBound' contract term.
    
    Defines the upper bound of the Maintenance Margin. If MRVM falls above MRMMU, then capital is refunded to reach the original MRIM.
    
**Acronym**: `MRMMU`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'maintenanceMarginUpperBound' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="maintenanceMarginUpperBound", value=value)

class MarketObjectCode(RiskFactorReferenceTerm):
    """Represents the 'marketObjectCode' contract term.
    
    Is pointing to the market value at SD (MarketObject).
Unique codes for market objects must be used.
    
**Acronym**: `MOC`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'marketObjectCode' must be one of str, got " + type(value).__name__)
        super().__init__(termName="marketObjectCode", value=value)

class MarketObjectCodeOfRateReset(RiskFactorReferenceTerm):
    """Represents the 'marketObjectCodeOfRateReset' contract term.
    
    Is pointing to the interest rate driver (MarketObject) used for rate reset uniquely.
Unique codes for market objects must be used.
    
**Acronym**: `RRMO`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'marketObjectCodeOfRateReset' must be one of str, got " + type(value).__name__)
        super().__init__(termName="marketObjectCodeOfRateReset", value=value)

class MarketObjectCodeOfScalingIndex(RiskFactorReferenceTerm):
    """Represents the 'marketObjectCodeOfScalingIndex' contract term.
    
**Acronym**: `SCMO`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'marketObjectCodeOfScalingIndex' must be one of str, got " + type(value).__name__)
        super().__init__(termName="marketObjectCodeOfScalingIndex", value=value)

class MarketValueObserved(ActusTerm):
    """Represents the 'marketValueObserved' contract term.
    
    Value as observed in the market at SD per unit. Incase of fixed income instruments it is a fraction.
    
**Acronym**: `MVO`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'marketValueObserved' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="marketValueObserved", value=value)

class MaturityDate(ActusTerm):
    """Represents the 'maturityDate' contract term.
    
    Marks the contractual end of the lifecycle of a CT. Generally, date of the last cash flows. 
This includes normally a principal and an interest payment. Some Maturity CTs as perpetuals (PBN) do not have such a date. For variable amortizing contracts of the ANN CT, this date might be less than the scheduled end of the contract (which is deduced from the periodic payment amount 
PRNXT). In this case it balloons.
    
**Acronym**: `MD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'maturityDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'maturityDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="maturityDate", value=value)

class MaximumPenaltyFreeDisbursement(ActusTerm):
    """Represents the 'maximumPenaltyFreeDisbursement' contract term.
    
    Defines the notional amount which can be withdrawn before XDN without penalty
    
**Acronym**: `MPFD`
    **Default**: `[ the value of notionalPrincipal ]`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'maximumPenaltyFreeDisbursement' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="maximumPenaltyFreeDisbursement", value=value)

class NextDividendPaymentAmount(ActusTerm):
    """Represents the 'nextDividendPaymentAmount' contract term.
    
    Defines the next dividend payment (amount) whereas the date of dividend payment is defined through the DVANX/DVCL pair. If DVCL is defined, then this amount will be used as dividend payment for each future dividend payment date.
    
**Acronym**: `DVNP`
    **Default**: `0`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'nextDividendPaymentAmount' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="nextDividendPaymentAmount", value=value)

class NextPrincipalRedemptionPayment(ActusTerm):
    """Represents the 'nextPrincipalRedemptionPayment' contract term.
    
    Amount of principal that will be paid during the redemption cycle at the next payment date. For amortizing contracts like ANN, NAM, ANX, and NAX this is the total periodic payment amount (sum of interest and principal).
    
**Acronym**: `PRNXT`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'nextPrincipalRedemptionPayment' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="nextPrincipalRedemptionPayment", value=value)

class NextResetRate(ActusTerm):
    """Represents the 'nextResetRate' contract term.
    
    Holds the new rate that has been fixed already (cf. attribute FixingDays) but not applied. This new rate will be applied at the next rate reset event (after SD and according to the rate reset schedule). Attention, RRNXT must be set to NULL after it is applied!
    
**Acronym**: `RRNXT`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'nextResetRate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="nextResetRate", value=value)

class NominalInterestRate(ActusTerm):
    """Represents the 'nominalInterestRate' contract term.
    
    The nominal interest rate which will be used to calculate accruals and the next interest payment at the next IP date. NT multiplied with IPNR is the base for the interest payment calculation. The relevant time period is a function of IPDC. 
If the contract is variable (RRANX set) this field is periodically updated per SD. 
In the case of plan vanilla interest rate swaps (IRSPV) this defines the rate of fixed leg.
    
**Acronym**: `IPNR`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'nominalInterestRate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="nominalInterestRate", value=value)

class NominalInterestRate2(ActusTerm):
    """Represents the 'nominalInterestRate2' contract term.
    
    The nominal interest rate which will be used to calculate accruals and the next interest payment at the next IP date on the second leg (the one not mentioned in CNTRL) of a plain vanilla swap. The relevant time period is a function of IPDC. 
It is periodically updated per SD.
    
**Acronym**: `IPNR2`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'nominalInterestRate2' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="nominalInterestRate2", value=value)

class NonPerformingDate(ActusTerm):
    """Represents the 'nonPerformingDate' contract term.
    
    The date of the (uncovered) payment event responsible for the current value of the Contract Performance attribute.
    
**Acronym**: `NPD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'nonPerformingDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'nonPerformingDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="nonPerformingDate", value=value)

class NotionalPrincipal(ActusTerm):
    """Represents the 'notionalPrincipal' contract term.
    
    Current nominal value of the contract. For debt instrument this is the current remaining notional outstanding. 
NT is generally the basis on which interest payments are calculated. If IPCBS is set, IPCBS may introduce a different basis for interest payment calculation.
    
**Acronym**: `NT`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'notionalPrincipal' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="notionalPrincipal", value=value)

class NotionalPrincipal2(ActusTerm):
    """Represents the 'notionalPrincipal2' contract term.
    
    Notional amount of the second currency to be exchanged in an FXOUT CT.
    
**Acronym**: `NT2`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'notionalPrincipal2' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="notionalPrincipal2", value=value)

class NotionalScalingMultiplier(ActusTerm):
    """Represents the 'notionalScalingMultiplier' contract term.
    
    The multiplier being applied to principal cash flows
    
**Acronym**: `SCNT`
    **Default**: `1`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'notionalScalingMultiplier' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="notionalScalingMultiplier", value=value)

class OptionExerciseEndDate(ActusTerm):
    """Represents the 'optionExerciseEndDate' contract term.
    
    Final exercise date for American and Bermudan options, expiry date for European options.
    
**Acronym**: `OPXED`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'optionExerciseEndDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'optionExerciseEndDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="optionExerciseEndDate", value=value)

class OptionExerciseType(ActusTerm):
    """Represents the 'optionExerciseType' contract term.
    
    Defines whether the option is European (exercised at a specific date), American (exercised during a span of time) or Bermudan (exercised at certain points during a span of time).
    
**Acronym**: `OPXT`
    **Default**: ``
    **Allowed Values:**
    - `european` (`E`): European-type exercise.
    - `bermudan` (`B`): Bermudan-type exercise.
    - `american` (`A`): American-type exercise."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'optionExerciseType' must be one of str, got " + type(value).__name__)
        super().__init__(termName="optionExerciseType", value=value)

class OptionStrike1(ActusTerm):
    """Represents the 'optionStrike1' contract term.
    
    Strike price of the option. Whether it is a call/put is determined by the attribute OPTP, i.e a call or a put (or a combination of call/put).
This attribute is used for price related options such as options on bonds, stocks or FX. Interest rate related options (caps/floos) are handled within th RatReset group.
    
**Acronym**: `OPS1`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'optionStrike1' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="optionStrike1", value=value)

class OptionStrike2(ActusTerm):
    """Represents the 'optionStrike2' contract term.
    
    Put price in case of call/put.
    
**Acronym**: `sss`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'optionStrike2' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="optionStrike2", value=value)

class OptionType(ActusTerm):
    """Represents the 'optionType' contract term.
    
    Defines whether the option is a call or put or a combination of it. This field has to be seen in combination with CNTRL where it is defined whether CRID is the buyer or the seller.
    
**Acronym**: `OPTP`
    **Default**: ``
    **Allowed Values:**
    - `call` (`C`): Call option.
    - `put` (`P`): Put option.
    - `callPut` (`CP`): Combination of call and put option."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'optionType' must be one of str, got " + type(value).__name__)
        super().__init__(termName="optionType", value=value)

class PenaltyRate(ActusTerm):
    """Represents the 'penaltyRate' contract term.
    
    Either the rate or the absolute amount of the prepayment.
    
**Acronym**: `PYRT`
    **Default**: `0`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'penaltyRate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="penaltyRate", value=value)

class PenaltyType(ActusTerm):
    """Represents the 'penaltyType' contract term.
    
    Defines whether prepayment is linked to a penalty and of which kind.
    
**Acronym**: `PYTP`
    **Default**: `O`
    **Allowed Values:**
    - `noPenalty` (`N`): No penalty applies.
    - `fixedPenalty` (`A`): A fixed amount applies as penalty.
    - `relativePenalty` (`R`): A penalty relative to the notional outstanding applies.
    - `interestRateDifferential` (`I`): A penalty based on the current interest rate differential relative to the notional outstanding applies."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'penaltyType' must be one of str, got " + type(value).__name__)
        super().__init__(termName="penaltyType", value=value)

class PeriodCap(ActusTerm):
    """Represents the 'periodCap' contract term.
    
    For variable rate basic CTs this represents the maximum positive rate change per rate reset cycle.
    
**Acronym**: `RRPC`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'periodCap' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="periodCap", value=value)

class PeriodFloor(ActusTerm):
    """Represents the 'periodFloor' contract term.
    
    For variable rate basic CTs this represents the maximum negative rate change per rate reset cycle.
    
**Acronym**: `RRPF`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'periodFloor' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="periodFloor", value=value)

class PremiumDiscountAtIED(ActusTerm):
    """Represents the 'premiumDiscountAtIED' contract term.
    
    Total original premium or discount that has been set at CDD and will be added to the (notional) cash flow at IED (cash flow at IED = NT+PDIED, w.r.t. an RPA CT). 
Negative value for discount and positive for premium.
Note, similar to interest the PDIED portion is part of P&L.
    
**Acronym**: `PDIED`
    **Default**: `0`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'premiumDiscountAtIED' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="premiumDiscountAtIED", value=value)

class PrepaymentEffect(ActusTerm):
    """Represents the 'prepaymentEffect' contract term.
    
    This attribute defines whether or not the right of prepayment exists and if yes, how prepayment affects the remaining principal redemption schedule of the contract
    
**Acronym**: `PPEF`
    **Default**: `N`
    **Allowed Values:**
    - `noPrepayment` (`N`): Prepayment is not allowed under the agreement.
    - `prepaymentReducesRedemptionAmount` (`A`): Prepayment is allowed and reduces the redemption amount for the remaining period up to maturity.
    - `prepaymentReducesMaturity` (`M`): Prepayment is allowed and reduces the maturity."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'prepaymentEffect' must be one of str, got " + type(value).__name__)
        super().__init__(termName="prepaymentEffect", value=value)

class PrepaymentPeriod(ActusTerm):
    """Represents the 'prepaymentPeriod' contract term.
    
    If real payment happens before scheduled payment date minus PPP, then it is considered a prepayment. Effect of prepayments are further described in PPEF and related fields.
    
**Acronym**: `PPP`
    **Default**: `P0D`
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'prepaymentPeriod' must be one of str, got " + type(value).__name__)
        super().__init__(termName="prepaymentPeriod", value=value)

class PriceAtPurchaseDate(ActusTerm):
    """Represents the 'priceAtPurchaseDate' contract term.
    
    Purchase price exchanged at PRD.  
PPRD represents a clean price (includes premium/discount but not IPAC).
    
**Acronym**: `PPRD`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'priceAtPurchaseDate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="priceAtPurchaseDate", value=value)

class PriceAtTerminationDate(ActusTerm):
    """Represents the 'priceAtTerminationDate' contract term.
    
    Sellingprice exchanged at PTD  PTDrepresents a clean price (includes premium/discount but not IPAC
    
**Acronym**: `PTD`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'priceAtTerminationDate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="priceAtTerminationDate", value=value)

class PurchaseDate(ActusTerm):
    """Represents the 'purchaseDate' contract term.
    
    If a contract is bought after initiation (for example a bond on the secondary market) this date has to be set. It refers to the date at which the payment (of PPRD) and transfer of the security happens. In other words, PRD - if set - takes the role otherwise IED has from a cash flow perspective. 
Note, CPID of the CT is not the counterparty of the transaction!
    
**Acronym**: `PRD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'purchaseDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'purchaseDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="purchaseDate", value=value)

class Quantity(ActusTerm):
    """Represents the 'quantity' contract term.
    
    This attribute relates either to physical contracts (COM) or underlyings of traded contracts. 
In case of physical contracts it holds the number of underlying units of the specific good (e.g. number of barrels of oil). 
In case of well defined traded contracts it holds the number of defined underlying instruments. Example: QT of STK CTs underlying a FUTUR indicates the number of those specific STK CTs which underlie the FUTUR.
    
**Acronym**: `QT`
    **Default**: `1`
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'quantity' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="quantity", value=value)

class RateMultiplier(ActusTerm):
    """Represents the 'rateMultiplier' contract term.
    
    Interest rate multiplier. A typical rate resetting rule is LIBOR plus x basis point where x represents the interest rate spread.
However, in some cases like reverse or super floater contracts an additional rate multiplier applies. In this case, the new rate is determined as: IPNR after rate reset = Rate selected from the market object * RRMLT + RRSP.
    
**Acronym**: `RRMLT`
    **Default**: `1`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'rateMultiplier' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="rateMultiplier", value=value)

class RateSpread(ActusTerm):
    """Represents the 'rateSpread' contract term.
    
    Interest rate spread. A typical rate resetting rule is LIBOR plus x basis point where x represents the interest rate spread.  
The following equation can be taken if RRMLT is not set: IPNR after rate reset = Rate selected from the market object  + RRSP.
    
**Acronym**: `RRSP`
    **Default**: `0`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'rateSpread' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="rateSpread", value=value)

class ScalingEffect(ActusTerm):
    """Represents the 'scalingEffect' contract term.
    
    Indicates which payments are scaled. I = Interest payments, N = Nominal payments and M = Maximum deferred interest amount. They can be scaled in any combination.
    
**Acronym**: `SCEF`
    **Default**: `000
`
    **Allowed Values:**
    - `noScaling` (`000`): No scaling applies.
    - `interestIsScaled` (`I00`): Scaling applies only to interest.
    - `principalIsScaled` (`0N0`): Scaling applies only to principal.
    - `interestAndPrincipalIsScaled` (`IN0`): Scaling applies to interest and principal."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'scalingEffect' must be one of str, got " + type(value).__name__)
        super().__init__(termName="scalingEffect", value=value)

class ScalingIndexAtContractDealDate(ActusTerm):
    """Represents the 'scalingIndexAtContractDealDate' contract term.
    
    The value of the Scaling Index as per Contract Deal Date.
    
**Acronym**: `SCCDD`
    **Default**: ``"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'scalingIndexAtContractDealDate' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="scalingIndexAtContractDealDate", value=value)

class Seniority(ActusTerm):
    """Represents the 'seniority' contract term.
    
    Refers to the order of repayment in the event of a sale or default of the issuer.
    
**Acronym**: `SEN`
    **Default**: ``
    **Allowed Values:**
    - `senior` (`S`): Contract represents senior debt.
    - `junior` (`J`): Contract represents junior debt."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'seniority' must be one of str, got " + type(value).__name__)
        super().__init__(termName="seniority", value=value)

class SettlementCurrency(ActusTerm):
    """Represents the 'settlementCurrency' contract term.
    
    The currency in which cash flows are settled. This currency can be different from the currency (CUR) in which cash flows or the contract, respectively, is denominated in which case the respective FX-rate applies at settlement time.
If no settlement currency is defined the cash flows are settled in the currency in which they are denominated.
    
**Acronym**: `CURS`
    **Default**: ``
    **Allowed Values:**
    - `ISO4217`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'settlementCurrency' must be one of str, got " + type(value).__name__)
        super().__init__(termName="settlementCurrency", value=value)

class SettlementPeriod(ActusTerm):
    """Represents the 'settlementPeriod' contract term.
    
    Defines the period from fixing of a contingent event/obligation (Exercise Date) to settlement of the obligation.
    
**Acronym**: `STP`
    **Default**: `P0D`
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'settlementPeriod' must be one of str, got " + type(value).__name__)
        super().__init__(termName="settlementPeriod", value=value)

class StatusDate(ActusTerm):
    """Represents the 'statusDate' contract term.
    
    SD holds the date per which all attributes of the record were updated. This is especially important for the highly dynamic attributes like Accruals, Notional, interest rates in variable instruments etc.
    
**Acronym**: `SD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'statusDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'statusDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="statusDate", value=value)

class TerminationDate(ActusTerm):
    """Represents the 'terminationDate' contract term.
    
    If a contract is sold before MD (for example a bond on the secondary market) this date has to be set. It refers to the date at which the payment (of PTD) and transfer of the security happens. In other words, TD - if set - takes the role otherwise MD has from a cash flow perspective. 
Note, CPID of the CT is not the counterparty of the transaction!
    
**Acronym**: `TD`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Datetime`"""
    def __init__(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("'terminationDate' must be a valid ISO 8601 string")
        else:
            raise TypeError("'terminationDate' must be a datetime or ISO 8601 string, got " + type(value).__name__)
        super().__init__(termName="terminationDate", value=value)

class Unit(ActusTerm):
    """Represents the 'unit' contract term.
    
    The physical unit of the contract. Example: Barrels for an Oil COM CT.
    
**Acronym**: `UT`
    **Default**: ``
    **Allowed Values:**
    - `barrel` (`BRL`): Physical unit of the contract is Barrels.
    - `bushel` (`BSH`): Physical unit of the contract is Bushel.
    - `gallon` (`GLN`): Physical unit of the contract is Gallons.
    - `currencyUnit` (`CUU`): Physical unit of the contract is Currency Units.
    - `megaWattHours` (`MWH`): Physical unit of the contract is Mega Watt Hours.
    - `pounds` (`PND`): Physical unit of the contract is Pounds.
    - `shortTons` (`STN`): Physical unit of the contract is Short Tons.
    - `tons` (`TON`): Physical unit of the contract is Tons.
    - `troyOunce` (`TRO`): Physical unit of the contract is Troy Ounces."""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'unit' must be one of str, got " + type(value).__name__)
        super().__init__(termName="unit", value=value)

class VariationMargin(ActusTerm):
    """Represents the 'variationMargin' contract term.
    
    MRVM reflects the accrued but not yet paid margin as per SD.  
Open traded positions are revalued by the exchange at the end of every trading day using mark-to-market valuation. Often clearing members do not credit or debit their clients daily with MRVM, but rather use a Maintenance Margin. If the balance falls outside MRMML (and MRMMU), then  capital must be added (is refunded) to reach the original margin amount MRIM. We can also say that MVO+MRVM is equal to the reference value as per last margin update.
    
**Acronym**: `MRVM`
    **Default**: ``
    **Allowed Values:**
    - `Positive`"""
    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("'variationMargin' must be one of float, int, got " + type(value).__name__)
        super().__init__(termName="variationMargin", value=value)

class XDayNotice(ActusTerm):
    """Represents the 'xDayNotice' contract term.
    
    Used as rolling attribute with the callable CT's UMP and CLM uniquely. CLM's and UMP's will not be settled (MD not set) until the client uses his option to call the contract X_Day_Notice after Current Date. As long as MD or TD is not set, the client postpones his right to call to the future. The cycle is normally defined in number of business days.
    
**Acronym**: `XDN`
    **Default**: ``
    **Allowed Values:**
    - `ISO8601 Duration`"""
    def __init__(self, value):
        if not isinstance(value, (str)):
            raise TypeError("'xDayNotice' must be one of str, got " + type(value).__name__)
        super().__init__(termName="xDayNotice", value=value)
