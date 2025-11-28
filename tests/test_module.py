import pandas as pd
import numpy as np
import pytest
from leadtimeutils.module import has_thursday_after_5_days, has_thursday_after_5_days_vectorized

def test_scalar_basic():
    # Start: Sun Oct 1, End: Tue Oct 10
    # Diff = 9 days. Start+5 = Fri Oct 6. Next Thu = Oct 12.
    # Oct 12 > Oct 10. Expected: False.
    start = pd.Timestamp("2023-10-01")
    end = pd.Timestamp("2023-10-10")
    assert has_thursday_after_5_days(start, end) == False

    # Start: Sun Oct 1, End: Sun Oct 15
    # Diff = 14 days. Start+5 = Fri Oct 6. Next Thu = Oct 12.
    # Oct 12 <= Oct 15. Expected: True.
    end = pd.Timestamp("2023-10-15")
    assert has_thursday_after_5_days(start, end) == True

def test_scalar_end_is_thursday():
    # Start: Sun Oct 1. End: Thu Oct 12.
    # End is Thursday. Logic says return False immediately.
    start = pd.Timestamp("2023-10-01")
    end = pd.Timestamp("2023-10-12")
    assert has_thursday_after_5_days(start, end) == False

def test_scalar_short_diff():
    # Start: Sun Oct 1. End: Wed Oct 4.
    # Diff = 3 days. < 5. Expected: False.
    start = pd.Timestamp("2023-10-01")
    end = pd.Timestamp("2023-10-04")
    assert has_thursday_after_5_days(start, end) == False

def test_vectorized_matches_scalar():
    # Create a range of dates to test various scenarios
    starts = pd.date_range("2023-01-01", periods=100, freq='D')
    ends = pd.date_range("2023-01-05", periods=100, freq='D')
    
    # Create a cross product or just random pairs? Let's do random pairs.
    np.random.seed(42)
    random_starts = np.random.choice(starts, 50)
    random_ends = np.random.choice(ends, 50)
    
    # Ensure end >= start
    final_starts = []
    final_ends = []
    for s, e in zip(random_starts, random_ends):
        if s > e:
            s, e = e, s
        final_starts.append(s)
        final_ends.append(e)
        
    df = pd.DataFrame({'start': final_starts, 'end': final_ends})
    
    # Run vectorized
    vec_results = has_thursday_after_5_days_vectorized(df, 'start', 'end')
    
    # Run scalar loop
    scalar_results = []
    for _, row in df.iterrows():
        scalar_results.append(has_thursday_after_5_days(row['start'], row['end']))
        
    np.testing.assert_array_equal(vec_results, scalar_results)

def test_vectorized_edge_cases():
    df = pd.DataFrame({
        'start': [pd.Timestamp("2023-10-01"), pd.NaT, pd.Timestamp("2023-10-01")],
        'end':   [pd.Timestamp("2023-10-15"), pd.Timestamp("2023-10-15"), pd.NaT]
    })
    results = has_thursday_after_5_days_vectorized(df, 'start', 'end')
    expected = np.array([True, False, False])
    np.testing.assert_array_equal(results, expected)
