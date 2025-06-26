# Auto-generated from actus-dictionary-applicability.json
# Do not edit manually. Used for business rule validation.

APPLICABILITY_RULES = {
  "annuity": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "amortizationDate",
      "businessDayConvention",
      "calendar",
      "capitalizationEndDate",
      "contractPerformance",
      "creditLineAmount",
      "cycleAnchorDateOfInterestPayment",
      "cycleOfInterestPayment",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "maturityDate",
      "nextPrincipalRedemptionPayment",
      "nonPerformingDate",
      "premiumDiscountAtIED",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "8": {
        "drivers": [
          "prepaymentEffect"
        ],
        "required": [],
        "optional": [
          "prepaymentPeriod",
          "optionExerciseEndDate",
          "cycleAnchorDateOfOptionality",
          "cycleOfOptionality",
          "penaltyType",
          "penaltyRate"
        ]
      },
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "3": {
        "drivers": [
          "interestCalculationBase"
        ],
        "required": [
          "interestCalculationBaseAmount"
        ],
        "optional": [
          "cycleAnchorDateOfInterestCalculationBase",
          "cycleOfInterestCalculationBase"
        ]
      },
      "4": {
        "drivers": [],
        "required": [],
        "optional": [
          "cycleAnchorDateOfPrincipalRedemption",
          "cycleOfPrincipalRedemption"
        ]
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "scalingEffect"
        ],
        "required": [
          "marketObjectCodeOfScalingIndex",
          "scalingIndexAtContractDealDate",
          "notionalScalingMultiplier",
          "interestScalingMultiplier"
        ],
        "optional": [
          "cycleAnchorDateOfScalingIndex",
          "cycleOfScalingIndex"
        ]
      },
      "9": {
        "drivers": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset"
        ],
        "required": [
          "rateSpread",
          "marketObjectCodeOfRateReset"
        ],
        "optional": [
          "lifeCap",
          "lifeFloor",
          "periodCap",
          "periodFloor",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "boundaryControlledSwitch": {
    "mandatory": [
      "boundaryDirection",
      "boundaryEffect",
      "boundaryLegInitiallyActive",
      "boundaryMonitoringAnchorDate",
      "boundaryMonitoringCycle",
      "boundaryMonitoringEndDate",
      "boundaryValue",
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "maturityDate",
      "priceAtPurchaseDate",
      "purchaseDate",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "deliverySettlement",
      "endOfMonthConvention",
      "marketObjectCode",
      "marketValueObserved",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      }
    }
  },
  "callMoney": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate",
      "xDayNotice"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "cycleAnchorDateOfInterestPayment",
      "cycleOfInterestPayment",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "maturityDate",
      "nonPerformingDate",
      "prepaymentPeriod",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "9": {
        "drivers": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset"
        ],
        "required": [
          "rateSpread",
          "marketObjectCodeOfRateReset"
        ],
        "optional": [
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "capFloor": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "statusDate"
    ],
    "standalone_optional": [
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [],
        "required": [],
        "optional": [
          "lifeCap",
          "lifeFloor"
        ]
      }
    }
  },
  "cash": {
    "mandatory": [
      "contractID",
      "contractRole",
      "contractType",
      "creatorID",
      "currency",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [],
    "conditional_groups": {}
  },
  "collateral": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "guaranteedExposure",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "coverageOfCreditEnhancement",
      "creditEventTypeCovered",
      "endOfMonthConvention",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "7": {
        "drivers": [
          "exerciseDate"
        ],
        "required": [
          "exerciseAmount"
        ],
        "optional": []
      }
    }
  },
  "commodity": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "creatorID",
      "currency",
      "priceAtPurchaseDate",
      "purchaseDate",
      "quantity",
      "statusDate",
      "unit"
    ],
    "standalone_optional": [
      "counterpartyID",
      "marketObjectCode",
      "marketValueObserved"
    ],
    "conditional_groups": {
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      }
    }
  },
  "exoticLinearAmortizer": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "capitalizationEndDate",
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "maturityDate",
      "nonPerformingDate",
      "premiumDiscountAtIED",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "8": {
        "drivers": [
          "prepaymentEffect"
        ],
        "required": [],
        "optional": [
          "prepaymentPeriod",
          "optionExerciseEndDate",
          "cycleAnchorDateOfOptionality",
          "cycleOfOptionality",
          "penaltyType",
          "penaltyRate"
        ]
      },
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "2": {
        "drivers": [
          "arrayCycleAnchorDateOfInterestPayment",
          "arrayCycleOfInterestPayment"
        ],
        "required": [],
        "optional": [
          "cyclePointOfInterestPayment"
        ]
      },
      "3": {
        "drivers": [
          "interestCalculationBase"
        ],
        "required": [
          "interestCalculationBaseAmount"
        ],
        "optional": [
          "cycleAnchorDateOfInterestCalculationBase",
          "cycleOfInterestCalculationBase"
        ]
      },
      "4": {
        "drivers": [
          "arrayCycleAnchorDateOfPrincipalRedemption",
          "arrayCycleOfPrincipalRedemption",
          "arrayNextPrincipalRedemptionPayment",
          "arrayIncreaseDecrease"
        ],
        "required": [],
        "optional": []
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "scalingEffect"
        ],
        "required": [
          "marketObjectCodeOfScalingIndex",
          "scalingIndexAtContractDealDate",
          "notionalScalingMultiplier",
          "interestScalingMultiplier"
        ],
        "optional": [
          "cycleAnchorDateOfScalingIndex",
          "cycleOfScalingIndex"
        ]
      },
      "9": {
        "drivers": [
          "arrayCycleAnchorDateOfRateReset"
        ],
        "required": [
          "arrayRate",
          "arrayFixedVariable",
          "marketObjectCodeOfRateReset"
        ],
        "optional": [
          "arrayCycleOfRateReset",
          "lifeCap",
          "lifeFloor",
          "periodCap",
          "periodFloor",
          "cyclePointOfRateReset",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "foreignExchangeOutright": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "currency2",
      "maturityDate",
      "notionalPrincipal",
      "notionalPrincipal2",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "deliverySettlement",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "exerciseDate"
        ],
        "required": [
          "exerciseAmount"
        ],
        "optional": []
      }
    }
  },
  "future": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "futuresPrice",
      "maturityDate",
      "priceAtPurchaseDate",
      "purchaseDate",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "deliverySettlement",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "initialMargin"
        ],
        "required": [
          "clearingHouse"
        ],
        "optional": [
          "maintenanceMarginLowerBound",
          "maintenanceMarginUpperBound",
          "cycleAnchorDateOfMargining",
          "cycleOfMargining",
          "variationMargin"
        ]
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "exerciseDate"
        ],
        "required": [
          "exerciseAmount"
        ],
        "optional": []
      }
    }
  },
  "guarantee": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "guaranteedExposure",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "coverageOfCreditEnhancement",
      "creditEventTypeCovered",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "maturityDate",
      "nonPerformingDate",
      "notionalPrincipal",
      "settlementCurrency",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "exerciseDate"
        ],
        "required": [
          "exerciseAmount"
        ],
        "optional": []
      }
    }
  },
  "linearAmortizer": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "capitalizationEndDate",
      "contractPerformance",
      "creditLineAmount",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "maturityDate",
      "nextPrincipalRedemptionPayment",
      "nonPerformingDate",
      "premiumDiscountAtIED",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "8": {
        "drivers": [
          "prepaymentEffect"
        ],
        "required": [],
        "optional": [
          "prepaymentPeriod",
          "optionExerciseEndDate",
          "cycleAnchorDateOfOptionality",
          "cycleOfOptionality",
          "penaltyType",
          "penaltyRate"
        ]
      },
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "2": {
        "drivers": [
          "cycleAnchorDateOfInterestPayment",
          "cycleOfInterestPayment"
        ],
        "required": [],
        "optional": [
          "cyclePointOfInterestPayment"
        ]
      },
      "3": {
        "drivers": [
          "interestCalculationBase"
        ],
        "required": [
          "interestCalculationBaseAmount"
        ],
        "optional": [
          "cycleAnchorDateOfInterestCalculationBase",
          "cycleOfInterestCalculationBase"
        ]
      },
      "4": {
        "drivers": [],
        "required": [],
        "optional": [
          "cycleAnchorDateOfPrincipalRedemption",
          "cycleOfPrincipalRedemption"
        ]
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "scalingEffect"
        ],
        "required": [
          "marketObjectCodeOfScalingIndex",
          "scalingIndexAtContractDealDate",
          "notionalScalingMultiplier",
          "interestScalingMultiplier"
        ],
        "optional": [
          "cycleAnchorDateOfScalingIndex",
          "cycleOfScalingIndex"
        ]
      },
      "9": {
        "drivers": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset"
        ],
        "required": [
          "rateSpread",
          "marketObjectCodeOfRateReset"
        ],
        "optional": [
          "lifeCap",
          "lifeFloor",
          "periodCap",
          "periodFloor",
          "cyclePointOfRateReset",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "negativeAmortizer": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "marketObjectCodeOfRateReset",
      "nextPrincipalRedemptionPayment",
      "nominalInterestRate",
      "notionalPrincipal",
      "rateSpread",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "capitalizationEndDate",
      "contractPerformance",
      "creditLineAmount",
      "cycleAnchorDateOfInterestPayment",
      "cycleOfInterestPayment",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "maturityDate",
      "nonPerformingDate",
      "premiumDiscountAtIED",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "8": {
        "drivers": [
          "prepaymentEffect"
        ],
        "required": [],
        "optional": [
          "prepaymentPeriod",
          "optionExerciseEndDate",
          "cycleAnchorDateOfOptionality",
          "cycleOfOptionality",
          "penaltyType",
          "penaltyRate"
        ]
      },
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "3": {
        "drivers": [
          "interestCalculationBase"
        ],
        "required": [
          "interestCalculationBaseAmount"
        ],
        "optional": [
          "cycleAnchorDateOfInterestCalculationBase",
          "cycleOfInterestCalculationBase"
        ]
      },
      "4": {
        "drivers": [],
        "required": [],
        "optional": [
          "cycleAnchorDateOfPrincipalRedemption",
          "cycleOfPrincipalRedemption"
        ]
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "scalingEffect"
        ],
        "required": [
          "marketObjectCodeOfScalingIndex",
          "scalingIndexAtContractDealDate",
          "notionalScalingMultiplier",
          "interestScalingMultiplier"
        ],
        "optional": [
          "cycleAnchorDateOfScalingIndex",
          "cycleOfScalingIndex"
        ]
      },
      "9": {
        "drivers": [],
        "required": [],
        "optional": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset",
          "lifeCap",
          "lifeFloor",
          "periodCap",
          "periodFloor",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "option": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "maturityDate",
      "optionExerciseEndDate",
      "optionExerciseType",
      "optionStrike1",
      "optionType",
      "priceAtPurchaseDate",
      "purchaseDate",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "cycleAnchorDateOfOptionality",
      "cycleOfOptionality",
      "delinquencyPeriod",
      "delinquencyRate",
      "deliverySettlement",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "optionStrike2",
      "seniority",
      "settlementCurrency",
      "settlementPeriod"
    ],
    "conditional_groups": {
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "exerciseDate"
        ],
        "required": [
          "exerciseAmount"
        ],
        "optional": []
      }
    }
  },
  "plainVanillaSwap": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "marketObjectCodeOfRateReset",
      "maturityDate",
      "nominalInterestRate",
      "nominalInterestRate2",
      "notionalPrincipal",
      "rateSpread",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "deliverySettlement",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "2": {
        "drivers": [
          "cycleAnchorDateOfInterestPayment",
          "cycleOfInterestPayment"
        ],
        "required": [],
        "optional": []
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "9": {
        "drivers": [],
        "required": [],
        "optional": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset",
          "cyclePointOfRateReset",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "principalAtMaturity": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "maturityDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "capitalizationEndDate",
      "contractPerformance",
      "creditLineAmount",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "premiumDiscountAtIED",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "8": {
        "drivers": [
          "prepaymentEffect"
        ],
        "required": [],
        "optional": [
          "prepaymentPeriod",
          "optionExerciseEndDate",
          "cycleAnchorDateOfOptionality",
          "cycleOfOptionality",
          "penaltyType",
          "penaltyRate"
        ]
      },
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "2": {
        "drivers": [
          "cycleAnchorDateOfInterestPayment",
          "cycleOfInterestPayment"
        ],
        "required": [],
        "optional": [
          "cyclePointOfInterestPayment"
        ]
      },
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "7": {
        "drivers": [
          "scalingEffect"
        ],
        "required": [
          "marketObjectCodeOfScalingIndex",
          "scalingIndexAtContractDealDate",
          "notionalScalingMultiplier",
          "interestScalingMultiplier"
        ],
        "optional": [
          "cycleAnchorDateOfScalingIndex",
          "cycleOfScalingIndex"
        ]
      },
      "9": {
        "drivers": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset"
        ],
        "required": [
          "rateSpread",
          "marketObjectCodeOfRateReset"
        ],
        "optional": [
          "lifeCap",
          "lifeFloor",
          "periodCap",
          "periodFloor",
          "cyclePointOfRateReset",
          "fixingPeriod",
          "nextResetRate",
          "rateMultiplier"
        ]
      }
    }
  },
  "stock": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "notionalPrincipal",
      "priceAtPurchaseDate",
      "purchaseDate",
      "quantity",
      "statusDate"
    ],
    "standalone_optional": [
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "endOfMonthConvention",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "cycleOfDividend",
          "nextDividendPaymentAmount"
        ],
        "required": [
          "cycleAnchorDateOfDividend"
        ],
        "optional": [
          "exDividendDate"
        ]
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      }
    }
  },
  "swap": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractStructure",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "statusDate"
    ],
    "standalone_optional": [
      "contractPerformance",
      "delinquencyPeriod",
      "delinquencyRate",
      "deliverySettlement",
      "gracePeriod",
      "marketObjectCode",
      "marketValueObserved",
      "nonPerformingDate",
      "seniority",
      "settlementCurrency"
    ],
    "conditional_groups": {
      "5": {
        "drivers": [
          "purchaseDate"
        ],
        "required": [
          "priceAtPurchaseDate"
        ],
        "optional": []
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      }
    }
  },
  "undefinedMaturityProfile": {
    "mandatory": [
      "contractDealDate",
      "contractID",
      "contractRole",
      "contractType",
      "counterpartyID",
      "creatorID",
      "currency",
      "dayCountConvention",
      "initialExchangeDate",
      "nominalInterestRate",
      "notionalPrincipal",
      "statusDate"
    ],
    "standalone_optional": [
      "accruedInterest",
      "businessDayConvention",
      "calendar",
      "contractPerformance",
      "cycleAnchorDateOfInterestPayment",
      "cycleOfInterestPayment",
      "delinquencyPeriod",
      "delinquencyRate",
      "endOfMonthConvention",
      "gracePeriod",
      "maximumPenaltyFreeDisbursement",
      "nonPerformingDate",
      "prepaymentPeriod",
      "seniority",
      "settlementCurrency",
      "xDayNotice"
    ],
    "conditional_groups": {
      "1": {
        "drivers": [
          "feeRate"
        ],
        "required": [
          "feeBasis"
        ],
        "optional": [
          "cycleAnchorDateOfFee",
          "cycleOfFee",
          "feeAccrued"
        ]
      },
      "6": {
        "drivers": [
          "terminationDate"
        ],
        "required": [
          "priceAtTerminationDate"
        ],
        "optional": []
      },
      "9": {
        "drivers": [
          "cycleAnchorDateOfRateReset",
          "cycleOfRateReset"
        ],
        "required": [
          "rateSpread",
          "marketObjectCodeOfRateReset"
        ],
        "optional": []
      }
    }
  }
}