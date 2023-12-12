def calculate_crc(input_bitstring, polynomial_bitstring):
    # Print mandatory information with copyright notice
    print("****************************************************************************************")
    print("* Copyright © 2023 Raihan Bin Mofidul. All rights reserved.                            *")
    print("* Unauthorized copying, modification, distribution, or use of this work is prohibited. *")
    print("****************************************************************************************")
    print()

    """Calculate the CRC for a given input bitstring and polynomial."""
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input, len_polynomial = len(input_bitstring), len(polynomial_bitstring)

    # Only applicable for Received Frame SOF~CRC
    if len_input > 32:
        SOF_DATA = input_bitstring[:-16]      # Exclude last 16 bits (15 bits CRC + 1 bit CRC delimiter)
        CRC      = input_bitstring[-15:]      # Extract 15-bit CRC
        input_bitstring = SOF_DATA + CRC

    # Pad the input with zeros
    input_padded_array = list(input_bitstring + '0' * (len_polynomial - 1))

    # Loop through each bit in the input
    for index in range(len_input):
        if input_padded_array[index] == '1':
            # XOR the polynomial with the input at specific intervals
            for i in range(len_polynomial):
                input_padded_array[index + i] = str(int(polynomial_bitstring[i] != input_padded_array[index + i]))

    # Extract the CRC from the padded array
    crc_binary = ''.join(input_padded_array)[-len_polynomial:]

    return crc_binary

def calculate_crc_without_cp_msg (input_bitstring, polynomial_bitstring):
    """Calculate the CRC for a given input bitstring and polynomial."""
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    len_input, len_polynomial = len(input_bitstring), len(polynomial_bitstring)

    # Only applicable for Received Frame SOF~CRC
    if len_input > 32:
        SOF_DATA = input_bitstring[:-16]      # Exclude last 16 bits (15 bits CRC + 1 bit CRC delimiter)
        CRC      = input_bitstring[-15:]      # Extract 15-bit CRC
        input_bitstring = SOF_DATA + CRC

    # Pad the input with zeros
    input_padded_array = list(input_bitstring + '0' * (len_polynomial - 1))

    # Loop through each bit in the input
    for index in range(len_input):
        if input_padded_array[index] == '1':
            # XOR the polynomial with the input at specific intervals
            for i in range(len_polynomial):
                input_padded_array[index + i] = str(int(polynomial_bitstring[i] != input_padded_array[index + i]))

    # Extract the CRC from the padded array
    crc_binary = ''.join(input_padded_array)[-len_polynomial:]

    return crc_binary

def binary_to_hex(binary_str):
    """Convert a binary string to a hexadecimal string."""
    return hex(int(binary_str, 2))

def hamming_distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strings must have the same length")
    distance = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            distance += 1
    return distance

def analyze_errors(transmitted_SOF_Data, crc_polynomial, error_positions):
    # ANSI escape code for red color
    RED = '\033[91m'
    RESET = '\033[0m'

    # Calculate Received CRC and Ensure CRCs are of the same length for comparison
    transmitted_crc_original = calculate_crc(transmitted_SOF_Data, crc_polynomial).zfill(15)

    # Calculate original Hamming distance
    original_hamming_distance  = hamming_distance(transmitted_crc_original, transmitted_crc_original)

    # Print error injection and comparison table header
    print("Hamming Distance with and without Error Injection:")
    print("============================================================================================================")
    print("| Error Position | Error Injected | Transmitted Frame [SOF~Data]     | Calculated [CRC] | Hamming Distance |")
    
    # Print original Hamming distance for reference
    print("|----------------|----------------|----------------------------------|------------------|------------------|")
    print(f"| [Original] N/A | {'No':14} | {transmitted_SOF_Data:15} | {transmitted_crc_original:12}  | {original_hamming_distance:16} |")

    # Insert errors and compare with received CRC
    print("|----------------|----------------|----------------------------------|------------------|------------------|")
    for pos in error_positions:
        error_message = list(transmitted_SOF_Data)
        if pos < len(error_message):
            error_message[pos]      = '1' if error_message[pos] == '0' else '0'
            error_crc               = calculate_crc_without_cp_msg("".join(error_message), crc_polynomial).zfill(15)
            error_hamming_distance  = hamming_distance(transmitted_crc_original, error_crc)

            # Highlight error position in red
            error_message_str = "".join(error_message)
            error_message_str = error_message_str[:pos] + RED + error_message_str[pos] + RESET + error_message_str[pos+1:]
            print(f"| {pos:14} | {'Yes':14} | {error_message_str:15} | {error_crc:12}  | {error_hamming_distance:16} |")
    print("============================================================================================================")