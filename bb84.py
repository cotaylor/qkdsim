import numpy as np
import qit
from utils import *

def bb84(n, verbose=True, eve=True):
    """Simulation of Bennett & Brassard's 1984 protocol for quantum key distribution with
    n initial bits in the raw key.
    If eavesdrop is set to True, assumes the presence of an eavesdropper attempting an
    intercept-resend attack.
    """
    numBits = 4*n
    
    if verbose:
        print("\n=====BB84 protocol=====\n%d initial bits, ~%d key bits") % (numBits, n)
        if eavesdrop: print("with eavesdropping")
        else: print("without eavesdropping\n")

    # Alice generates a random bit string to be encoded
    rawKey = getRandomBits(numBits)

    # Alice also randomly chooses which basis to use when encoding each bit
    # 0: computational basis; 1: Hadamard basis
    bases_A = getRandomBits(numBits)

    print("\nAlice generates %d random bits to be encoded:\n%s") % (numBits, bitFormat(rawKey))
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

    # QKD guarantees with high probability we will detect any eavesdropping
    if eve:
        if verbose:
            print("Eve intercepts each qubit as it travels to Bob. Because it is not possible"\
                  "\nto clone quantum states, she must measure each qubit before re-sending to"\
                  "\nBob. Every time she measures a qubit in the 'wrong' basis, she has a 50%"\
                  "\nprobability of being detected.\n")

        # No matter what strategy Eve uses to select bases, the probability she will be detected
        # is always 1-(3/4)^numBits if Alice chose her bases randomly
        bases_E = getRandomBits(numBits)
        print("Eve chooses a random basis to measure each qubit in:\n%s") % bitFormat(bases_E)

        # Eve measures each qubit and attempts to cover her tracks
        for k in range(numBits):
            sent_A[k] = eavesdrop(sent_A[k], bases_E[k])

        if verbose: print("\nEve attempts to hide her actions by re-encoding her measurement result"\
                          "\nbefore re-sending the qubits to Bob.\n")

    # Bob measures qubit each in a randomly chosen basis
    bases_B = getRandomBits(numBits)
    key_B = []
    for k in range(numBits):
        key_B.append(decodeState(sent_A[k], bases_B[k]))

    print("Bob chooses a random basis to measure each qubit in:\n%s") % bitFormat(bases_B)
    print("Bob's measurement results:\n%s") % bitFormat(key_B)

    # Alice and Bob discard any bits where they chose different bases.
    key_A, key_B = matchKeys(rawKey, key_B, bases_A, bases_B)
    numBits = len(key_A)

    if verbose:
        print("\nBob announces when he has measured the last qubit and discloses"\
              "\nthe bases he used for each measurement. Alice and Bob then discard"\
              "\nany bits where they chose different bases.\n")

    print("Alice's key after discarding mismatches:\n%s") % bitFormat(key_A)
    print("Bob's key after discarding mismatches:\n%s") % bitFormat(key_B)

    # Alice and Bob sacrifice a subset of their bits to try to detect Eve
    # TODO: can examine effect of announcing more or fewer bits
    announce_A, key_A, announce_B, key_B = discloseHalf(key_A, key_B)
    if verbose:
        print("\nAlice and Bob sacrifice %d of their %d shared bits and publicly announce"\
              "\ntheir values. They agree to disclose every other bit of their shared key.\n") % (len(announce_A), numBits)

    print("Alice's announced bits:\n%s") % bitFormat(announce_A)
    print("Bob's announced bits:\n%s") % bitFormat(announce_B)

    # TODO: add possibility of channel noise
    if announce_A != announce_B:
        print("\nAlice and Bob detect Eve's interference and abort the protocol.")
        return 1

    numBits = len(key_A)
    print("Alice's remaining %d-bit key:\n%s") % (numBits, bitFormat(key_A))
    print("Bob's remaining %d-bit key:\n%s") % (numBits, bitFormat(key_B))

    return 0
