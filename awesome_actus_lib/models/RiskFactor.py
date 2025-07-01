import re
from abc import ABC, abstractmethod
from datetime import date, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from collections import Counter


class RiskFactor(ABC):
    """
    Abstract base class for all types of risk factors (e.g., yield curves, indices).
    """
    def __init__(self, marketObjectCode: str, source):
        self.marketObjectCode = marketObjectCode
        self._data = None
        self.loadData(source)

    def loadData(self, source):
        """
        Load data from a pandas DataFrame or a CSV file path.
        """
        if isinstance(source, pd.DataFrame):
            self._data = source.copy()
        elif isinstance(source, str):
            try:
                self._data = pd.read_csv(source)
            except Exception as e:
                raise ValueError(f"Failed to read risk factor data from '{source}': {e}")
        else:
            raise TypeError("loadData expects a pandas DataFrame or a file path (str).")

    def plot(self, title=None, figsize=(10, 5), return_fig=False):
        """
        Plots the risk factor's rate over time.

        Args:
            title (str, optional): Title of the plot. Defaults to the class name and marketObjectCode.
            figsize (tuple): Size of the plot figure.
            return_fig (bool): If True, returns the matplotlib figure object instead of showing.
        """
        if self._data is None or 'value' not in self._data.columns:
            raise ValueError("No data to plot or missing 'value' column.")

        df = self._data.copy()
        df['date'] = pd.to_datetime(df['date'])

        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(df['date'], df['value'], marker='o')

        default_title = f"{self.__class__.__name__} - {self.marketObjectCode}"
        ax.set_title(title or default_title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Rate / Value")
        ax.grid(True)
        plt.tight_layout()

        if return_fig:
            return fig
        else:
            plt.show()

        


    def _validate_and_format_dates(self, date_column: str = "date") -> pd.Series:
        """
        Validates and normalizes a date column to ISO format.
        If the column doesn't exist but the index is a datetime index, it will be used instead.
        Accepts 'date' or 'Date' as valid column names.
        """
        if date_column not in self._data.columns:
            # Try case-insensitive matching
            alt_column = None
            for col in self._data.columns:
                if col.lower() == date_column.lower():
                    alt_column = col
                    break

            if alt_column:
                date_column = alt_column
            elif isinstance(self._data.index, pd.DatetimeIndex):
                self._data = self._data.reset_index().rename(columns={"index": date_column})
            else:
                raise ValueError(
                    f"Missing expected '{date_column}' column, and index is not a DatetimeIndex.\n"
                    f"Hint: Either provide a '{date_column}' column (case-insensitive) or use a DatetimeIndex."
                )

        self._data[date_column] = pd.to_datetime(self._data[date_column])
        


        def try_parse(d):
            try:
                return pd.to_datetime(d).strftime("%Y-%m-%d")
            except Exception:
                raise ValueError(f"Invalid date format: '{d}'. Expected ISO format like 'YYYY-MM-DD'.")

        return self._data[date_column].apply(try_parse)


    @abstractmethod
    def to_json(self):
        """
        Serialize the risk factor data to JSON (to be used by event generation).
        Must be implemented by subclasses.
        """

    def __repr__(self):
        return f"<{self.__class__.__name__} code='{self.marketObjectCode}' rows={len(self._data) if self._data is not None else 0}>"

    def __str__(self):
        preview = self._data.head() if self._data is not None else "No data loaded"
        return f"RiskFactor: {self.marketObjectCode}\n{preview}"

    


class ReferenceIndex(RiskFactor):
    """
    Concrete subclass representing a time series of reference index values.
    Expected columns: ['date', 'value'] with ISO8601-formatted date strings.
    """

    def __init__(self, marketObjectCode: str, source, base: int = 1):
        self.base = base
        super().__init__(marketObjectCode, source)

    def to_json(self):
        if self._data is None:
            return {}

        df = self._data.copy()
        df['date'] = self._validate_and_format_dates("date")

        
        if 'value' in df.columns:
            value_col = 'value'
        elif 'Value' in df.columns:
            value_col = 'Value'
        elif 'rate' in df.columns:
            value_col = 'rate'
        elif 'Rate' in df.columns:
            value_col = 'Rate'
        else:
            raise ValueError("ReferenceIndex data must contain a 'value' or 'Rate' column.")

        return {
            "marketObjectCode": self.marketObjectCode,
            "base": self.base,
            "data": [
                {"time": f"{date}T00:00:00", "value": float(value)}
                for date, value in zip(df['date'], df[value_col])
            ]
        }


class YieldCurve(RiskFactor):
    """
    Concrete subclass representing a yield curve as date-value pairs derived from tenors.
    Expected input: referenceDate, tenors (e.g., ['1M', '3M', '1Y']), and rates.
    """

    def __init__(self, marketObjectCode: str, referenceDate: str, tenors: list[str], rates: list[float], base: int = 1):
        self.base = base
        self.referenceDate = pd.to_datetime(referenceDate).date()
        self.tenors = tenors
        self.rates = rates
        self._validate_inputs()
        df = self._tenors_to_dataframe()
        super().__init__(marketObjectCode, df)

    def _validate_inputs(self):
        if len(self.tenors) != len(self.rates):
            raise ValueError("Tenors and rates must be of the same length.")
        
        duplicates = [tenor for tenor, count in Counter(self.tenors).items() if count > 1]
        if duplicates:
            raise ValueError(f"Tenors must be unique. Duplicated entries: {', '.join(duplicates)}")

        for t in self.tenors:
            if not re.fullmatch(r"\d+[DWMY]", t):
                raise ValueError(f"Invalid tenor format: '{t}'. Use e.g., '3M', '1Y', '7D'.")

    def _tenors_to_dataframe(self) -> pd.DataFrame:
        dates = [self._add_tenor(self.referenceDate, tenor) for tenor in self.tenors]
        return pd.DataFrame({"date": dates, "value": self.rates})

    def _add_tenor(self, start_date: date, tenor: str) -> date:
        number = int(tenor[:-1])
        unit = tenor[-1].upper()

        if unit == 'D':
            return start_date + timedelta(days=number)
        elif unit == 'W':
            return start_date + timedelta(weeks=number)
        elif unit == 'M':
            return start_date + relativedelta(months=number)
        elif unit == 'Y':
            return start_date + relativedelta(years=number)
        else:
            raise ValueError(f"Unsupported tenor unit: '{unit}'")

    def to_json(self):
        if self._data is None:
            return {}

        df = self._data.copy()
        df['date'] = self._validate_and_format_dates("date")

        return {
            "marketObjectCode": self.marketObjectCode,
            "base": self.base,
            "data": [
                {"time": f"{date}T00:00:00", "value": float(value)}
                for date, value in zip(df["date"], df["value"])
            ]
        }