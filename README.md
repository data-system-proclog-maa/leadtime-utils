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

## Usage

```python
import pandas as pd
import numpy as np
import leadtimeutils as ltu
```

## Available Functions

```
has_thursday_after_5_days(start_date, end_date)
```
checks if thursday exists at least 5 days after the start date and before the end date.

```
has_thursday_after_5_days_vectorized(df, start_col, end_col)
```
fast vectorized version for entire DataFrames.

```
get_days_between(df, start_col, end_col)
```
returns the list of day names between two dates for each row.


## Scalar check
```
start = pd.Timestamp("2023-10-01")
end = pd.Timestamp("2023-10-15")
result = ltu.has_thursday_after_5_days(start, end)
print(result)
```

## Vectorized check
```
df = pd.DataFrame({
    'start': [pd.Timestamp("2023-10-01")],
    'end': [pd.Timestamp("2023-10-15")]
})
results = ltu.has_thursday_after_5_days_vectorized(df, 'start', 'end')
print(results)
```
