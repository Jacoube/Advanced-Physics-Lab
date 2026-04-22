import pandas as pd
import numpy as np

###################################################
### FOR B1 (DAY 1): CALCULATING T1 FOR PROTONS
###################################################

def find_closest_index(df, delay = 0, column_name='TIME'):
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

def max_at_trigger(df, delay = 0):
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

###################################################
### FOR B2 (DAY 2): 
###################################################

def find_closest_index_delay(df, delay = 250, column_name='TIME'):
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
    return closest_index + delay

def max_at_trigger_delay(df, delay = 250):
    """ 
    Calculate the maximum value of the amplitude at the trigger point. CH1 is the full wave
    data while CH2 is the averaged maximum.

    Args:
    df: Pandas dataframe containing CH1 and CH2 data.

    Returns:
    (ch1, ch2): Tuple containing the value of CH1 and CH2 at the trigger point.
    """
    idx_at_trig = find_closest_index_delay(df, delay)

    # Looking at CH1 (Full Wave Form)
    ch1_max = df['CH1'][idx_at_trig] # Test switching from CH1 to CH1 Peak Detect

    # Looking at CH2 (Should be max output)
    ch2_max = df['CH2'][idx_at_trig]
    return (ch1_max, ch2_max)

def max_at_trigger_avg(df, freq, delay = 250):
    """ 
    Calculate the maximum value of the amplitude at the trigger point by averaging the abs of the points around it by the frequency. 
    CH1 is the full wave data while CH2 is the averaged maximum.

    Args:
    df: Pandas dataframe containing CH1 and CH2 data.

    Returns:
    (ch1, ch2): Tuple containing the value of CH1 and CH2 at the trigger point.
    """
    idx_at_trig = find_closest_index_delay(df, delay)

    # Looking at CH1 (Full Wave Form)
    ch1_list = df['CH1'][idx_at_trig:idx_at_trig + int(1 / freq / .000032)] # Test switching from CH1 to CH1 Peak Detect
    ch1_max = max(map(abs, ch1_list))

    # Looking at CH2 (Should be max output)
    ch2_list = df['CH2'][idx_at_trig:idx_at_trig + int(1 / freq / .000032)] # Test switching from CH1 to CH1 Peak Detect
    ch2_max = max(map(abs, ch2_list))
    return (ch1_max, ch2_max)