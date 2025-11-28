import pandas as pd
# Note: In your installed environment, you would import from leadtimeutils
# from leadtimeutils import module
# For local testing within this repo, we might need to adjust path or install locally
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'leadtime-utils'))
from leadtimeutils import module

# Example 1: Scalar usage
start = pd.Timestamp("2023-10-01") # Sunday
end = pd.Timestamp("2023-10-10")   # Tuesday (9 days later)
result = module.has_thursday_after_5_days(start, end)
print(f"Scalar check ({start.date()} to {end.date()}): {result}")

# Example 2: Vectorized usage with DataFrame
data = {
    'start_date': [
        '2023-10-01', # Sunday
        '2023-10-01',
        '2023-11-01'
    ],
    'end_date': [
        '2023-10-10', 
        '2023-10-15', 
        '2023-11-02'
    ]
}
df = pd.DataFrame(data)
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

print("\nDataFrame Input:")
print(df)

# Apply vectorized function
# Note: The module expects column names as strings
df['has_thursday'] = module.has_thursday_after_5_days_vectorized(df, 'start_date', 'end_date')

# Get days between
df['days_list'] = module.get_days_between(df, 'start_date', 'end_date')

print("\nDataFrame Output:")
print(df[['start_date', 'end_date', 'has_thursday', 'days_list']])
