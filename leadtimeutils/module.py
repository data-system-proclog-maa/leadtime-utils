import pandas as pd
import numpy as np
from typing import Union, List, Optional

def has_weekday_in_range(df: pd.DataFrame, start_date_col: str, end_date_col: str, chosen_day: int, main_days: int) -> np.ndarray:
    """
    Check whether a given weekday occurs in the date range
    [start_date + main_days, end_date], excluding rows where
    the end_date is the chosen weekday.

    This function works vectorized on the entire DataFrame.

    Args:
        df (pd.DataFrame): The dataframe containing the dates.
        start_date_col (str): The name of the start date column.
        end_date_col (str): The name of the end date column.
        chosen_day (int): the number for chosen days, (0=monday .... 6=sunday)
        main_days (int): minimum days after staryt_date before checking

    Returns:
        np.ndarray: A boolean array indicating if the condition is met for each row.
    """

    # validate input
    if not (isinstance(chosen_day, int) and 0<=chosen_day<=6):
        raise ValueError("chosen_day must be an integer between 0 and 6 (0=monday .... 6=sunday)")
    if not (isinstance(main_days, int) and main_days>=0):
        raise ValueError("main_days must be a non-negative integer")

    
    # parse date
    if start_date_col not in df.columns:
        raise KeyError (f"start_date_col {start_date_col} not found in dataframe")
    if end_date_col not in df.columns:
        raise KeyError (f"end_date_col {end_date_col} not found in dataframe")

    start = pd.to_datetime(df[start_date_col], errors='coerce')
    end = pd.to_datetime(df[end_date_col], errors='coerce')
    
    # condition 0: dates must be valid
    valid_dates = start.notna() & end.notna()
    
    # condition 1: end date is not chosen day
    not_end_chosen_day = end.dt.weekday != chosen_day
    
    # condition 2: diff >= main_days days
    diff_ge_main_days = (end - start).dt.days >= main_days

    base_mask = valid_dates & not_end_chosen_day & diff_ge_main_days
    if not base_mask.any():
        return np.zeros(len(df), dtype=bool)
    
    # compute earliest allowed day
    start_plus_main_days = start + pd.Timedelta(days=main_days)
    
    # compute number of days until chosen_days
    days_until_chosen_day = (chosen_day - start_plus_main_days.dt.weekday) % 7
    
    # first hit day
    first_valid_chosen_day = start_plus_main_days + pd.to_timedelta(days_until_chosen_day, unit='D')
    
    # check if this Thursday is <= end
    has_valid_chosen_day = first_valid_chosen_day <= end
    
    # combine all conditions
    result = (base_mask & has_valid_chosen_day)
    
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
