import numpy as np
import qit
from utils import *

def bb84(n, verbose=True, eavesdrop=True):
    """Simulation of Bennett & Brassard's 1984 protocol for quantum key distribution with
    n initial bits in the raw key.
    If eavesdrop is set to True, assumes the presence of an eavesdropper attempting an
    intercept-resend attack.
    """    
    if verbose:
        print("\n=====BB84 protocol=====\n%d initial bits") % n
        if eavesdrop: print("in the presence of an eavesdropper")
        else: print("without eavesdropping\n")

    # Alice generates a random bit string to be encoded
    rawKey = getRandomBits(n)

    # Alice also randomly chooses which basis to use when encoding each bit
    # 0: computational basis; 1: Hadamard basis
    bases_A = getRandomBits(n)

    print("\nAlice generates %d random bits to be encoded:\n%s") % (n, bitFormat(rawKey))
    print("For each bit, Alice randomly chooses one of two non-orthogonal sets of bases:\n%s") % bitFormat(bases_A)

    if verbose:
        print("\nAlice encodes each qubit according to the following strategy:"\
              "\n    value | basis | state"\
              "\n      0   |   0   | +1 |0>"\
              "\n      0   |   1   | +0.7071 (|0> + |1>)"\
              "\n      1   |   0   | +1 |1>"\
              "\n      1   |   1   | +0.7071 (|0> - |1>)"\
              "\nShe then sends each qubit one by one to Bob over a quantum channel.\n")

    # Alice prepares n qubits, with the kth qubit in state |0> or |1> in either the computational
    # basis or the Hadamard basis, depending on the value of the kth bit in each bitstring
    sent_A = encodeRawKey(rawKey, bases_A)

    # Bob measures qubit each in a randomly chosen basis
    bases_B = getRandomBits(n)
    key_B = []
    for k in range(n):
        key_B.append(decodeState(sent_A[k], bases_B[k]))

    print("For each qubit received, Bob randomly chooses a basis to measure in:\n%s") % bitFormat(bases_B)
    print("Bob's measurement results:\n%s") % bitFormat(key_B)

    # Alice and Bob discard any bits where they chose different bases.
    key_A, key_B = matchKeys(rawKey, key_B, bases_A, bases_B)

    if verbose:
        print("\nBob announces when he has measured the last qubit and discloses"\
              "\nthe bases he used for each measurement. Alice and Bob then discard"\
              "\nany bits where they chose different bases.\n")

    print("Alice's key after discarding mismatches:\n%s") % bitFormat(key_A)
    print("Bob's key after discarding mismatches:\n%s") % bitFormat(key_B)

    if (key_A == key_B): print("equal")
    else: print("not equal")
