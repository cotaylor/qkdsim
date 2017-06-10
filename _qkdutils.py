import numpy as np
from Crypto.Random import random
import qit

MAX_PRINT_SIZE = 56

def bitFormat(bits):
    """Return a printable representation of the given list of bools representing bits."""
    if len(bits) < MAX_PRINT_SIZE:
        out = ', '.join(['1' if b == True else '0' if b == False else '-' for b in bits])
        return '[' + out + ']'
    else:
        binaryString = ""
        for j in range(len(bits)):
            if bits[j]:
                binaryString += "1"
            else: binaryString += "0"
        return hex(int(binaryString, 2))

def detectEavesdrop(key1, key2, errorRate):
    """Return True if Alice and Bob detect Eve's interference, False otherwise."""
    if len(key1) == 0 or len(key2) == 0:
        return True
    if len(key1) != len(key2):
        return True

    tolerance = errorRate * 1.2
    mismatch = sum([1 for k in range(len(key1)) if key1[k] != key2[k]])
    if abs((float(mismatch) / len(key1)) - errorRate) > tolerance:
        return True

    return False

def discloseHalf(key1, key2):
    """Return the tuple (announce1, keep1, announce2, keep2), where
           announce2, announce2 = bit values to announce and discard
           keep1, keep2 = bit values of new shared keys
    """
    # Disclose every other bit
    announce1 = [key1[j] for j in range(len(key1)) if j % 2 == 0]
    keep1 = [key1[j] for j in range(len(key1)) if j % 2]
    announce2 = [key2[j] for j in range(len(key2)) if j % 2 == 0]
    keep2 = [key2[j] for j in range(len(key2)) if j % 2]
    return (announce1, keep1, announce2, keep2)

def equivState(state1, state2):
    """Return True if state1 and state2 represent the same quantum state."""
    return np.array_equal(state1.prob(), state2.prob())

def getRandomBits(length):
    """Return a list of bits with given length, each either 0 or 1 with equal probability."""
    bitstring = []
    for j in range(length):
        bitstring.append(random.choice([True, False]))
    return bitstring
