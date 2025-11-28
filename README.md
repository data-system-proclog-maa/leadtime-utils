# Lead Time Utils

A utility module for lead time analysis, specifically designed for handling business logic related to date calculations and constraints (e.g., Thursday constraints).

## Installation

```bash
pip install leadtimeutils
```

## Usage

```python
import pandas as pd
import leadtimeutils as ltu

# Scalar check
start = pd.Timestamp("2023-10-01")
end = pd.Timestamp("2023-10-15")
result = ltu.has_thursday_after_5_days(start, end)
print(result)

# Vectorized check
df = pd.DataFrame({
    'start': [pd.Timestamp("2023-10-01")],
    'end': [pd.Timestamp("2023-10-15")]
})
results = ltu.has_thursday_after_5_days_vectorized(df, 'start', 'end')
print(results)
```
