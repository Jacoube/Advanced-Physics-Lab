import numpy as np
import matplotlib.pyplot as plt
import math

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions for Part 1: Measuring steady-state behavior with a sine-driven LRC circuit
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def resonance_curve(omega, gamma, omega_0):
    """
    Calculates the amplitude ratio V_C / V_0.
    
    Parameters:
    omega   : array-like, Independent variable (angular frequency, ω)
    gamma   : float, Fitting parameter (R/L)
    omega_0 : float, Fitting parameter (resonant frequency, 1/sqrt(LC))
    """
    numerator = omega_0**2
    denominator = np.sqrt((gamma**2 * omega**2) + (omega**2 - omega_0**2)**2)
    return numerator / denominator

def calculate_gamma(R, L):
    return R / L

def calculate_omega_0(L, C):
    return 1 / (np.sqrt(L * C))

def calculate_omega_res(R, L, C):
    omega_0 = calculate_omega_0(L, C)
    gamma = calculate_gamma(R, L)
    return (np.sqrt(omega_0**2 - gamma**2 / 2))

def calculate_freq_0(L, C):
    omega_0 = calculate_omega_0(L, C)
    return omega_0 / (2 * np.pi)

def calculate_freq_res(R, L, C):
    omega_res = calculate_omega_res(R, L, C)
    return omega_res / (2 * np.pi)

def calculate_capacitance_uncertainty_1khz(value_farads):
    """
    Calculates uncertainty for Keysight U1733C at 1kHz.
    Based on datasheet specifications for C at 1kHz.
    """
    val = value_farads
    # Convert to appropriate units for range checking
    pf = val * 1e12
    nf = val * 1e9
    uf = val * 1e6
    mf = val * 1e3

    # Accuracy table for 1kHz (U1733C)
    # Range | Resolution | Accuracy (% + counts)
    if pf < 20: 
        return "Below Range"
    elif pf <= 200:
        accuracy_pct, counts, res = 0.2, 5, 1e-14 # 0.01pF res
    elif nf <= 2:
        accuracy_pct, counts, res = 0.2, 3, 1e-13 # 0.1pF res
    elif nf <= 20:
        accuracy_pct, counts, res = 0.2, 3, 1e-12 # 1pF res
    elif nf <= 200:
        accuracy_pct, counts, res = 0.2, 3, 1e-11 # 0.01nF res
    elif uf <= 2:
        accuracy_pct, counts, res = 0.2, 3, 1e-10 # 0.1nF res
    elif uf <= 20:
        accuracy_pct, counts, res = 0.2, 3, 1e-9  # 1nF res
    elif uf <= 200:
        accuracy_pct, counts, res = 0.5, 5, 1e-8  # 0.01uF res
    elif uf <= 2000:
        accuracy_pct, counts, res = 0.5, 8, 1e-7  # 0.1uF res
    else:
        return "1kHz not specified for >2000uF (Use 100Hz/120Hz)"

    uncertainty = (val * (accuracy_pct / 100)) + (counts * res)
    return uncertainty

def calculate_resistance_uncertainty_1khz(value_ohms):
    """
    Calculates uncertainty for Keysight U1733C Resistance at 1kHz.
    """
    val = value_ohms
    
    # Range check and accuracy assignment
    if val < 2:
        # Range 2 Ohm: 0.7% + 50 counts
        accuracy_pct, counts, res = 0.7, 50, 0.0001
    elif val < 20:
        # Range 20 Ohm: 0.7% + 8 counts
        accuracy_pct, counts, res = 0.7, 8, 0.001
    elif val < 200:
        # Range 200 Ohm: 0.2% + 3 counts
        accuracy_pct, counts, res = 0.2, 3, 0.01
    elif val < 2000:
        accuracy_pct, counts, res = 0.2, 3, 0.1
    elif val < 20000:
        accuracy_pct, counts, res = 0.2, 3, 1
    elif val < 200000:
        accuracy_pct, counts, res = 0.2, 3, 10
    elif val < 2000000:
        accuracy_pct, counts, res = 0.2, 3, 100
    elif val < 20000000:
        # Range 20 MOhm: 0.5% + 5 counts
        accuracy_pct, counts, res = 0.5, 5, 1000
    elif val <= 200000000:
        # Range 200 MOhm: 2.0% + 8 counts
        accuracy_pct, counts, res = 2.0, 8, 10000
    else:
        return "Out of Range (>200 MOhm)"

    uncertainty = (val * (accuracy_pct / 100)) + (counts * res)
    return uncertainty

def calculate_inductance_uncertainty_1khz(value_henries, print_output: bool = True): # TODO: Adjust these functions so they print out the correct num of sig figs
    """
    Calculates uncertainty for Keysight U1733C Inductance (L) at 1kHz.
    Based on datasheet specifications for L at 1kHz.
    """
    val = value_henries
    # Convert to common units for range checking
    uh = val * 1e6
    mh = val * 1e3
    h = val

    # Accuracy table for 1kHz (U1733C)
    # Range | Resolution | Accuracy (% + counts)
    if uh < 20:
        return "Below Range (< 20uH)"
    elif uh <= 200:
        # Note: Requires NULL for lead inductance
        accuracy_pct, counts, res = 1.0, 5, 1e-8    # 0.01uH res
    elif uh <= 2000:
        # Note: Requires NULL for lead inductance
        accuracy_pct, counts, res = 0.5, 3, 1e-7    # 0.1uH res
    elif mh <= 20:
        accuracy_pct, counts, res = 0.2, 3, 1e-6    # 0.001mH res
    elif mh <= 200:
        accuracy_pct, counts, res = 0.2, 3, 1e-5    # 0.01mH res
    elif mh <= 2000:
        accuracy_pct, counts, res = 0.2, 3, 1e-4    # 0.1mH res
    elif h <= 20:
        accuracy_pct, counts, res = 0.2, 3, 1e-3     # 0.001H res
    elif h <= 200:
        accuracy_pct, counts, res = 0.5, 5, 1e-2     # 0.01H res
    elif h <= 2000:
        accuracy_pct, counts, res = 1.0, 10, 1e-1    # 0.1H res
    else:
        return "Out of Range (> 2000H)"

    uncertainty = (val * (accuracy_pct / 100)) + (counts * res)

    if print_output:
        # 1. Get the exponent of the measurement (e.g., 0.015 -> -2)
        exponent = math.floor(math.log10(abs(value_henries)))
        
        # 2. Normalize both values to that specific power
        scaled_val = value_henries / (10**exponent)
        scaled_unc = uncertainty / (10**exponent)
        
        # 3. Print with the fixed exponent suffix
        print(f"Inductance: ({scaled_val:.4f} +/- {scaled_unc:.4f})e{exponent:04d} H")

    return uncertainty

    # Print ranges of Freq res at the extremes of the measured values

import numpy as np
import math

def calculate_frequency_bounds(R, L, C):
    # 1. Calculate individual uncertainties using previous functions
    u_R = calculate_resistance_uncertainty_1khz(R)
    u_L = calculate_inductance_uncertainty_1khz(L, print_output=False) # TODO: Adjust all functions to have the print output option
    u_C = calculate_capacitance_uncertainty_1khz(C)

    # 2. Define the Min/Max bounds for each component
    L_min, L_max = L - u_L, L + u_L
    C_min, C_max = C - u_C, C + u_C
    R_min, R_max = R - u_R, R + u_R

    # 3. Calculate Freq_0 Bounds (1 / (2*pi*sqrt(LC)))
    # Max freq occurs when L and C are smallest
    f0_min = 1 / (2 * np.pi * np.sqrt(L_max * C_max))
    f0_max = 1 / (2 * np.pi * np.sqrt(L_min * C_min))
    f0_meas = 1 / (2 * np.pi * np.sqrt(L * C))

    # 4. Calculate Freq_res Bounds (1 / (2*pi)) * sqrt((1/LC) - (R^2 / 2L^2))
    def get_f_res(r_val, l_val, c_val):
        term1 = 1 / (l_val * c_val)
        term2 = (r_val**2) / (2 * l_val**2)
        # Check for overdamping (if term2 > term1, resonance doesn't exist)
        if term2 >= term1: return 0 
        return (1 / (2 * np.pi)) * np.sqrt(term1 - term2)

    fres_meas = get_f_res(R, L, C)
    # F_res is minimized when R is large, L is large, and C is large
    fres_min = get_f_res(R_max, L_max, C_max)
    # F_res is maximized when R is small, L is small, and C is small
    fres_max = get_f_res(R_min, L_min, C_min)

    # 5. Formatting Helper (from our previous conversation)
    def print_aligned(label, nominal, minimum, maximum):
        u_total = (maximum - minimum) / 2
        exponent = math.floor(math.log10(abs(nominal)))
        scale = 10**exponent
        print(f"{label}: ({(nominal/scale):.3f} +/- {(u_total/scale):.3f})e{exponent:02d} Hz")
        print(f"   [Range: {minimum:.2f} to {maximum:.2f} Hz]\n")

    print("--- Frequency Uncertainty Analysis ---")
    print_aligned("Freq_0  ", f0_meas, f0_min, f0_max)
    print_aligned("Freq_res", fres_meas, fres_min, fres_max)

    return {"f0": (f0_min, f0_max), "fres": (fres_min, fres_max)}