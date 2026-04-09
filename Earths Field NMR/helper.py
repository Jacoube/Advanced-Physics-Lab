import pandas as pd
import numpy as np

###################################################
### FOR B1 (DAY 1): CALCULATING T1 FOR PROTONS
###################################################

def find_closest_index(df, column_name='TIME'):
    """
    Finds the index for the value in the specified column that is closest to 0. For the purpose of EFNMR, this
    is used to find the trigger point.

    Args:
    df: Pandas dataframe
    Optional:
    column_name: (Default to 'TIME) the column in the df to look at

    Returns:
    closest_index: Index closest to 0
    """
    # Calculate the absolute difference from 0 and find the index of the minimum
    # .idxmin() returns the index label of the first occurrence of the minimum value
    closest_index = df[column_name].abs().idxmin()
    return closest_index

def max_at_trigger(df):
    """ 
    Calculate the maximum value of the amplitude at the trigger point. CH1 is the full wave
    data while CH2 is the averaged maximum.

    Args:
    df: Pandas dataframe containing CH1 and CH2 data.

    Returns:
    (ch1, ch2): Tuple containing the value of CH1 and CH2 at the trigger point.
    """
    idx_at_trig = find_closest_index(df)

    # Looking at CH1 (Full Wave Form)
    ch1_max = df['CH1'][idx_at_trig]

    # Looking at CH2 (Should be max output)
    ch2_max = df['CH2'][idx_at_trig]
    return (ch1_max, ch2_max)