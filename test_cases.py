"""
LeetCode Test Cases Module
==========================
This module contains test data and validation functions for LeetCode problems.
Students can import this module to test their solutions.

Problems included:
1. Combine Two Tables (175)
2. Roman to Integer (13)
3. Duplicate Emails (182)
4. Game Play Analysis I (511)
5. Reshape Data: Concatenate (2888)
6. Invalid Tweets (1683)
7. Reshape Data: Pivot (2889)
8. Biggest Single Number (619)
"""

import pandas as pd
import numpy as np
from typing import Callable, Union


# ============================================================================
# Problem 1: Combine Two Tables (175)
# ============================================================================

def get_combine_two_tables_data():
    """
    Returns test data for Combine Two Tables problem.
    
    Returns:
        tuple: (person_df, address_df)
    """
    person = pd.DataFrame({
        'personId': [1, 2],
        'lastName': ['Wang', 'Alice'],
        'firstName': ['Allen', 'Bob']
    })
    
    address = pd.DataFrame({
        'addressId': [1, 2],
        'personId': [2, 3],
        'city': ['New York City', 'Leetcode'],
        'state': ['New York', 'California']
    })
    
    return person, address


def get_combine_two_tables_expected():
    """Returns expected output for Combine Two Tables problem."""
    return pd.DataFrame({
        'firstName': ['Allen', 'Bob'],
        'lastName': ['Wang', 'Alice'],
        'city': [None, 'New York City'],
        'state': [None, 'New York']
    })


def test_combine_two_tables(solution_func: Callable) -> bool:
    """
    Test the Combine Two Tables solution.
    
    Args:
        solution_func: Function that takes (person_df, address_df) and returns result DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    person, address = get_combine_two_tables_data()
    result = solution_func(person.copy(), address.copy())
    expected = get_combine_two_tables_expected()
    
    # Sort both DataFrames for comparison
    result_sorted = result.sort_values('firstName').reset_index(drop=True)
    expected_sorted = expected.sort_values('firstName').reset_index(drop=True)
    
    # Check columns
    if set(result.columns) != set(expected.columns):
        print(f"❌ Column mismatch! Expected: {list(expected.columns)}, Got: {list(result.columns)}")
        return False
    
    # Check values (handling None/NaN)
    result_sorted = result_sorted[expected.columns]
    
    try:
        # Replace None with NaN for comparison
        result_sorted = result_sorted.fillna(np.nan)
        expected_sorted = expected_sorted.fillna(np.nan)
        
        for col in expected.columns:
            for i in range(len(expected_sorted)):
                exp_val = expected_sorted.loc[i, col]
                res_val = result_sorted.loc[i, col]
                
                # Handle NaN comparison
                if pd.isna(exp_val) and pd.isna(res_val):
                    continue
                elif exp_val != res_val:
                    print(f"❌ Value mismatch at row {i}, column '{col}'! Expected: {exp_val}, Got: {res_val}")
                    return False
        
        print("✅ All tests passed for Combine Two Tables!")
        return True
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        return False


# ============================================================================
# Problem 2: Roman to Integer (13)
# ============================================================================

def get_roman_to_integer_test_cases():
    """
    Returns test cases for Roman to Integer problem.
    
    Returns:
        list: List of tuples (input, expected_output)
    """
    return [
        ("III", 3),
        ("LVIII", 58),
        ("MCMXCIV", 1994),
        ("IV", 4),
        ("IX", 9),
        ("XL", 40),
        ("XC", 90),
        ("CD", 400),
        ("CM", 900),
        ("MMXXIII", 2023),
        ("I", 1),
        ("MMMCMXCIX", 3999),
    ]


def test_roman_to_integer(solution_func: Callable) -> bool:
    """
    Test the Roman to Integer solution.
    
    Args:
        solution_func: Function that takes a roman numeral string and returns integer
    
    Returns:
        bool: True if all tests pass
    """
    test_cases = get_roman_to_integer_test_cases()
    all_passed = True
    
    for roman, expected in test_cases:
        result = solution_func(roman)
        if result != expected:
            print(f"❌ Failed: {roman} -> Expected {expected}, Got {result}")
            all_passed = False
        else:
            print(f"✓ Passed: {roman} = {result}")
    
    if all_passed:
        print("\n✅ All tests passed for Roman to Integer!")
    else:
        print("\n❌ Some tests failed for Roman to Integer!")
    
    return all_passed


# ============================================================================
# Problem 3: Duplicate Emails (182)
# ============================================================================

def get_duplicate_emails_data():
    """
    Returns test data for Duplicate Emails problem.
    
    Returns:
        DataFrame: Person table with id and email
    """
    return pd.DataFrame({
        'id': [1, 2, 3],
        'email': ['a@b.com', 'c@d.com', 'a@b.com']
    })


def get_duplicate_emails_expected():
    """Returns expected output for Duplicate Emails problem."""
    return pd.DataFrame({
        'Email': ['a@b.com']
    })


def test_duplicate_emails(solution_func: Callable) -> bool:
    """
    Test the Duplicate Emails solution.
    
    Args:
        solution_func: Function that takes person_df and returns result DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    person = get_duplicate_emails_data()
    result = solution_func(person.copy())
    expected = get_duplicate_emails_expected()
    
    # Normalize column names for comparison (case-insensitive)
    result.columns = result.columns.str.lower()
    expected.columns = expected.columns.str.lower()
    
    result_set = set(result['email'].values)
    expected_set = set(expected['email'].values)
    
    if result_set == expected_set:
        print("✅ All tests passed for Duplicate Emails!")
        return True
    else:
        print(f"❌ Expected: {expected_set}, Got: {result_set}")
        return False


# ============================================================================
# Problem 4: Game Play Analysis I (511)
# ============================================================================

def get_game_play_analysis_data():
    """
    Returns test data for Game Play Analysis I problem.
    
    Returns:
        DataFrame: Activity table
    """
    return pd.DataFrame({
        'player_id': [1, 1, 2, 3, 3],
        'device_id': [2, 2, 3, 1, 4],
        'event_date': pd.to_datetime(['2016-03-01', '2016-05-02', '2017-06-25', '2016-03-02', '2018-07-03']),
        'games_played': [5, 6, 1, 0, 5]
    })


def get_game_play_analysis_expected():
    """Returns expected output for Game Play Analysis I problem."""
    return pd.DataFrame({
        'player_id': [1, 2, 3],
        'first_login': pd.to_datetime(['2016-03-01', '2017-06-25', '2016-03-02'])
    })


def test_game_play_analysis(solution_func: Callable) -> bool:
    """
    Test the Game Play Analysis I solution.
    
    Args:
        solution_func: Function that takes activity_df and returns result DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    activity = get_game_play_analysis_data()
    result = solution_func(activity.copy())
    expected = get_game_play_analysis_expected()
    
    # Sort both DataFrames by player_id
    result_sorted = result.sort_values('player_id').reset_index(drop=True)
    expected_sorted = expected.sort_values('player_id').reset_index(drop=True)
    
    # Convert dates to same format for comparison
    result_sorted['first_login'] = pd.to_datetime(result_sorted['first_login'])
    expected_sorted['first_login'] = pd.to_datetime(expected_sorted['first_login'])
    
    try:
        pd.testing.assert_frame_equal(result_sorted, expected_sorted, check_dtype=False)
        print("✅ All tests passed for Game Play Analysis I!")
        return True
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False


# ============================================================================
# Problem 5: Reshape Data: Concatenate (2888)
# ============================================================================

def get_concatenate_data():
    """
    Returns test data for Reshape Data: Concatenate problem.
    
    Returns:
        tuple: (df1, df2)
    """
    df1 = pd.DataFrame({
        'student_id': [1, 2, 3, 4],
        'name': ['Mason', 'Ava', 'Taylor', 'Georgia'],
        'age': [8, 6, 15, 17]
    })
    
    df2 = pd.DataFrame({
        'student_id': [5, 6],
        'name': ['Leo', 'Alex'],
        'age': [7, 7]
    })
    
    return df1, df2


def get_concatenate_expected():
    """Returns expected output for Reshape Data: Concatenate problem."""
    return pd.DataFrame({
        'student_id': [1, 2, 3, 4, 5, 6],
        'name': ['Mason', 'Ava', 'Taylor', 'Georgia', 'Leo', 'Alex'],
        'age': [8, 6, 15, 17, 7, 7]
    })


def test_concatenate(solution_func: Callable) -> bool:
    """
    Test the Reshape Data: Concatenate solution.
    
    Args:
        solution_func: Function that takes (df1, df2) and returns concatenated DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    df1, df2 = get_concatenate_data()
    result = solution_func(df1.copy(), df2.copy())
    expected = get_concatenate_expected()
    
    # Reset index for comparison
    result = result.reset_index(drop=True)
    expected = expected.reset_index(drop=True)
    
    try:
        pd.testing.assert_frame_equal(result, expected, check_dtype=False)
        print("✅ All tests passed for Reshape Data: Concatenate!")
        return True
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False


# ============================================================================
# Problem 6: Invalid Tweets (1683)
# ============================================================================

def get_invalid_tweets_data():
    """
    Returns test data for Invalid Tweets problem.
    
    Returns:
        DataFrame: Tweets table
    """
    return pd.DataFrame({
        'tweet_id': [1, 2],
        'content': ['Let us Code', 'More than fifteen chars are here!']
    })


def get_invalid_tweets_expected():
    """Returns expected output for Invalid Tweets problem."""
    return pd.DataFrame({
        'tweet_id': [2]
    })


def test_invalid_tweets(solution_func: Callable) -> bool:
    """
    Test the Invalid Tweets solution.
    
    Args:
        solution_func: Function that takes tweets_df and returns result DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    tweets = get_invalid_tweets_data()
    result = solution_func(tweets.copy())
    expected = get_invalid_tweets_expected()
    
    result_set = set(result['tweet_id'].values)
    expected_set = set(expected['tweet_id'].values)
    
    if result_set == expected_set:
        print("✅ All tests passed for Invalid Tweets!")
        return True
    else:
        print(f"❌ Expected: {expected_set}, Got: {result_set}")
        return False


# ============================================================================
# Problem 7: Reshape Data: Pivot (2889)
# ============================================================================

def get_pivot_data():
    """
    Returns test data for Reshape Data: Pivot problem.
    
    Returns:
        DataFrame: Weather table
    """
    return pd.DataFrame({
        'city': ['Jacksonville', 'Jacksonville', 'Jacksonville', 'Jacksonville', 'Jacksonville',
                 'ElPaso', 'ElPaso', 'ElPaso', 'ElPaso', 'ElPaso'],
        'month': ['January', 'February', 'March', 'April', 'May',
                  'January', 'February', 'March', 'April', 'May'],
        'temperature': [13, 23, 38, 5, 34, 20, 6, 26, 2, 43]
    })


def get_pivot_expected():
    """Returns expected output for Reshape Data: Pivot problem."""
    return pd.DataFrame({
        'month': ['April', 'February', 'January', 'March', 'May'],
        'ElPaso': [2, 6, 20, 26, 43],
        'Jacksonville': [5, 23, 13, 38, 34]
    })


def test_pivot(solution_func: Callable) -> bool:
    """
    Test the Reshape Data: Pivot solution.
    
    Args:
        solution_func: Function that takes weather_df and returns pivoted DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    weather = get_pivot_data()
    result = solution_func(weather.copy())
    expected = get_pivot_expected()
    
    # Sort both DataFrames by month
    result_sorted = result.sort_values('month').reset_index(drop=True)
    expected_sorted = expected.sort_values('month').reset_index(drop=True)
    
    # Check if month column exists
    if 'month' not in result.columns:
        print("❌ 'month' column not found in result!")
        return False
    
    # Check city columns exist
    for city in ['ElPaso', 'Jacksonville']:
        if city not in result.columns:
            print(f"❌ '{city}' column not found in result!")
            return False
    
    # Compare values
    result_sorted = result_sorted[['month', 'ElPaso', 'Jacksonville']]
    
    try:
        pd.testing.assert_frame_equal(result_sorted, expected_sorted, check_dtype=False)
        print("✅ All tests passed for Reshape Data: Pivot!")
        return True
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False


# ============================================================================
# Problem 8: Biggest Single Number (619)
# ============================================================================

def get_biggest_single_number_data_1():
    """Returns first test data for Biggest Single Number problem."""
    return pd.DataFrame({
        'num': [8, 8, 3, 3, 1, 4, 5, 6]
    })


def get_biggest_single_number_data_2():
    """Returns second test data for Biggest Single Number problem (all duplicates)."""
    return pd.DataFrame({
        'num': [8, 8, 7, 7, 3, 3, 3]
    })


def test_biggest_single_number(solution_func: Callable) -> bool:
    """
    Test the Biggest Single Number solution.
    
    Args:
        solution_func: Function that takes my_numbers_df and returns result DataFrame
    
    Returns:
        bool: True if all tests pass
    """
    all_passed = True
    
    # Test case 1: Has single numbers
    data1 = get_biggest_single_number_data_1()
    result1 = solution_func(data1.copy())
    
    if result1['num'].iloc[0] != 6:
        print(f"❌ Test 1 failed: Expected 6, Got {result1['num'].iloc[0]}")
        all_passed = False
    else:
        print("✓ Test 1 passed: Correctly found 6 as the biggest single number")
    
    # Test case 2: No single numbers (all duplicates)
    data2 = get_biggest_single_number_data_2()
    result2 = solution_func(data2.copy())
    
    if result2['num'].iloc[0] is not None and not pd.isna(result2['num'].iloc[0]):
        print(f"❌ Test 2 failed: Expected None/null, Got {result2['num'].iloc[0]}")
        all_passed = False
    else:
        print("✓ Test 2 passed: Correctly returned null when no single number exists")
    
    if all_passed:
        print("\n✅ All tests passed for Biggest Single Number!")
    else:
        print("\n❌ Some tests failed for Biggest Single Number!")
    
    return all_passed


# ============================================================================
# Run All Tests
# ============================================================================

def run_all_tests(solutions: dict) -> None:
    """
    Run all tests for provided solutions.
    
    Args:
        solutions: Dictionary mapping problem names to solution functions
            Expected keys:
            - 'combine_two_tables'
            - 'roman_to_integer'
            - 'duplicate_emails'
            - 'game_play_analysis'
            - 'concatenate'
            - 'invalid_tweets'
            - 'pivot'
            - 'biggest_single_number'
    """
    print("=" * 60)
    print("Running All LeetCode Tests")
    print("=" * 60)
    
    test_funcs = {
        'combine_two_tables': test_combine_two_tables,
        'roman_to_integer': test_roman_to_integer,
        'duplicate_emails': test_duplicate_emails,
        'game_play_analysis': test_game_play_analysis,
        'concatenate': test_concatenate,
        'invalid_tweets': test_invalid_tweets,
        'pivot': test_pivot,
        'biggest_single_number': test_biggest_single_number
    }
    
    results = {}
    for problem_name, test_func in test_funcs.items():
        if problem_name in solutions:
            print(f"\n{'=' * 40}")
            print(f"Testing: {problem_name}")
            print('=' * 40)
            results[problem_name] = test_func(solutions[problem_name])
        else:
            print(f"\n⚠️  No solution provided for: {problem_name}")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    passed = sum(results.values())
    total = len(results)
    print(f"Passed: {passed}/{total}")


if __name__ == "__main__":
    print("LeetCode Test Cases Module")
    print("Import this module and use the test functions to validate your solutions.")
    print("\nExample usage:")
    print("  from test_cases import test_combine_two_tables, get_combine_two_tables_data")
    print("  person, address = get_combine_two_tables_data()")
    print("  # Define your solution function")
    print("  test_combine_two_tables(your_solution)")
