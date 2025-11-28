import pandas as pd
import numpy as np
from typing import Union, List, Optional

def has_thursday_after_5_days(start_date: pd.Timestamp, end_date: pd.Timestamp) -> bool:
    """
    Checks if there is a Thursday occurring at least 5 days after the start_date
    and on or before the end_date.

    Args:
        start_date (pd.Timestamp): The start date.
        end_date (pd.Timestamp): The end date.

    Returns:
        bool: True if the condition is met, False otherwise.
    """
    if pd.isna(start_date) or pd.isna(end_date):
        return False

    # exclude if the end date is thursday
    if end_date.weekday() == 3:  # 3 = Thursday
        return False

    day_diff = (end_date - start_date).days
    if day_diff < 5:
        return False

    # generate all days between start and end
    days = pd.date_range(start_date, end_date)

    # check if there's a thursday occurring *after* 5 days from start
    return any((d.weekday() == 3) and ((d - start_date).days >= 5) for d in days)


def has_thursday_after_5_days_vectorized(df: pd.DataFrame, start_date_col: str, end_date_col: str) -> np.ndarray:
    """
    Vectorized version of has_thursday_after_5_days.

    Args:
        df (pd.DataFrame): The dataframe containing the dates.
        start_date_col (str): The name of the start date column.
        end_date_col (str): The name of the end date column.

    Returns:
        np.ndarray: A boolean array indicating if the condition is met for each row.
    """
    start = pd.to_datetime(df[start_date_col], errors='coerce')
    end = pd.to_datetime(df[end_date_col], errors='coerce')
    
    # Condition 0: Dates must be valid
    valid_dates = start.notna() & end.notna()
    
    # Condition 1: End date is not Thursday
    not_end_thursday = end.dt.weekday != 3
    
    # Condition 2: Diff >= 5 days
    diff_ge_5 = (end - start).dt.days >= 5
    
    # Condition 3: There exists a Thursday T such that:
    # start + 5 days <= T <= end
    
    start_plus_5 = start + pd.Timedelta(days=5)
    
    # Find the first Thursday >= start_plus_5
    # days_until_thursday = (3 - weekday) % 7
    days_until_thursday = (3 - start_plus_5.dt.weekday) % 7
    first_valid_thursday = start_plus_5 + pd.to_timedelta(days_until_thursday, unit='D')
    
    # Check if this Thursday is <= end
    has_valid_thursday = first_valid_thursday <= end
    
    # Combine all conditions
    # We use fillna(False) to handle any NaTs that might have propagated
    result = (valid_dates & not_end_thursday & diff_ge_5 & has_valid_thursday).fillna(False)
    
    return result.to_numpy()


def get_days_between(df: pd.DataFrame, start_date_col: str, end_date_col: str) -> np.ndarray:
    """
    Returns a list of day names between start_date and end_date for each row.

    Args:
        df (pd.DataFrame): The dataframe.
        start_date_col (str): Start date column name.
        end_date_col (str): End date column name.

    Returns:
        np.ndarray: An object array where each element is a list of day names (strings).
    """
    start = pd.to_datetime(df[start_date_col], errors='coerce')
    end = pd.to_datetime(df[end_date_col], errors='coerce')

    valid = start.notna() & end.notna()
    
    out = np.empty(len(df), dtype=object)
    out[:] = None
    
    # This part is inherently iterative because the result is a list of variable length
    # But we can iterate only over valid rows
    idxs = np.where(valid)[0]
    for idx in idxs:
        rng = pd.date_range(start.iloc[idx], end.iloc[idx])
        out[idx] = rng.strftime('%A').tolist()

    return out

if __name__ == '__main__':
    print("module.py is a utility module for lead time analysis on mineral alam abadi procurement & logistic division")
