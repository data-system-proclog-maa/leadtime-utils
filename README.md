# Lead Time Utils

![PyPI Version](https://img.shields.io/badge/PyPI-1.0.0-blue)
![Python Versions](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

a utility module for lead time analysis, specifically designed for handling business logic related to date calculations and constraints internally in procurement & logistic division mineral alam abadi.

## Installation

```bash
pip install leadtimeutils
```

## Quick Start

```python
import pandas as pd
import numpy as np
import leadtimeutils as ltu
```

## Available Functions

### `has_weekday_in_range()`

Checks whether a specific weekday occurs within a date range, with a minimum number of days after the start date.

**Signature:**
```python
has_weekday_in_range(
    df: pd.DataFrame,
    start_date_col: str,
    end_date_col: str,
    chosen_day: int,
    main_days: int
) -> np.ndarray
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame containing the date columns
- `start_date_col` (str): Name of the start date column
- `end_date_col` (str): Name of the end date column
- `chosen_day` (int): Weekday to check for (0=Monday, 1=Tuesday, ..., 6=Sunday)
- `main_days` (int): Minimum number of days after start_date before checking for the weekday

**Returns:**
- `np.ndarray`: Boolean array indicating whether the condition is met for each row

**Behavior:**
- Returns `True` if the chosen weekday occurs between `start_date + main_days` and `end_date`
- Returns `False` if the end_date itself is the chosen weekday
- Handles invalid dates gracefully (returns `False` for those rows)

---

### `get_days_between()`

Returns a list of day names between two dates for each row.

**Signature:**
```python
get_days_between(
    df: pd.DataFrame,
    start_date_col: str,
    end_date_col: str
) -> np.ndarray
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame containing the date columns
- `start_date_col` (str): Name of the start date column
- `end_date_col` (str): Name of the end date column

**Returns:**
- `np.ndarray`: Object array where each element is a list of day names (e.g., `['Monday', 'Tuesday', ...]`)

---

## Usage Examples

### Example 1: Check for Thursday After 5 Days

```python
import pandas as pd
import leadtimeutils as ltu

df = pd.DataFrame({
    'start': ['2023-10-01', '2023-10-05'],
    'end': ['2023-10-15', '2023-10-08']
})

# Check if Thursday (day 3) occurs at least 5 days after start
results = ltu.has_weekday_in_range(df, 'start', 'end', chosen_day=3, main_days=5)
print(results)  # [True, False]
```

### Example 2: Check for Monday After 7 Days

```python
df = pd.DataFrame({
    'first_date': ['2023-11-01', '2023-11-10'],
    'end_date': ['2023-11-15', '2023-11-20']
})

# Check if Monday (day 0) occurs at least 7 days after order
results = ltu.has_weekday_in_range(df, 'first_date', 'end_date', chosen_day=0, main_days=7)
print(results)
```

### Example 3: Check for Friday After 3 Days

```python
df = pd.DataFrame({
    'first_date': ['2023-12-01'],
    'end_date': ['2023-12-10']
})

# Check if Friday (day 4) occurs at least 3 days after request
results = ltu.has_weekday_in_range(df, 'first_date', 'end_date', chosen_day=4, main_days=3)
print(results)
```

### Example 4: Get All Days Between Dates

```python
df = pd.DataFrame({
    'first_date': ['2023-10-01'],
    'end_date': ['2023-10-05']
})

day_lists = ltu.get_days_between(df, 'first_date', 'end_date')
print(day_lists[0])  # ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
```

---

## Weekday Reference

Use these values for the `chosen_day` parameter:

| Day       | Value |
|-----------|-------|
| Monday    | 0     |
| Tuesday   | 1     |
| Wednesday | 2     |
| Thursday  | 3     |
| Friday    | 4     |
| Saturday  | 5     |
| Sunday    | 6     |

---

## Migration Guide (v0.1.x → v0.2.0)

### Breaking Changes

The hardcoded `has_thursday_after_5_days()` functions have been replaced with a flexible `has_weekday_in_range()` function.

**Old (v0.1.x):**
```python
# Scalar version
result = ltu.has_thursday_after_5_days(start, end)

# Vectorized version
results = ltu.has_thursday_after_5_days_vectorized(df, 'start_col', 'end_col')
```

**New (v0.2.0):**
```python
# Unified vectorized function
results = ltu.has_weekday_in_range(df, 'start_col', 'end_col', chosen_day=3, main_days=5)
```

### Migration Steps

1. Replace `has_thursday_after_5_days_vectorized()` calls with `has_weekday_in_range()`
2. Add `chosen_day=3` (for Thursday) and `main_days=5` parameters
3. For scalar checks, create a single-row DataFrame first

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Fajar Amry** (nagabonar27)  
Email: faajaramry@gmail.com

## Repository

- Homepage: [https://github.com/data-system-proclog-maa/leadtime-utils](https://github.com/data-system-proclog-maa/leadtime-utils)
- Issues: [https://github.com/data-system-proclog-maa/leadtime-utils/issues](https://github.com/data-system-proclog-maa/leadtime-utils/issues)
