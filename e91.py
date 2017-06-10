from math import pi, cos, sqrt
import numpy as np
from Crypto.Random import random

def chooseAxes(numBits):
    """Return Alice and Bob's randomly chosen mstment axes for the specified
       number of qubits in the E91 protocol:
           A chooses from (0, pi/4, pi/2) with equal probability,
           B chooses from (pi/4, pi/2, 3pi/4) with equal probability.
    """
    choicesA = [0, pi/8, pi/4]
    choicesB = [0, pi/8, -pi/8]
    basesA = []
    basesB = []
    for j in range(numBits):
        basesA.append(random.choice(choicesA))
        basesB.append(random.choice(choicesB))

    return (basesA, basesB)

def formatBasesForPrint(bases):
    """Return printable representation of E91 basis choices for Alice and Bob.
           value | angle
             1   |   0
             2   |  pi/8
             3   |  pi/4
             4   | -pi/8
    """
    out = []
    for j in range(len(bases)):
        if bases[j] == 0:
            out.append(1)
        elif bases[j] == pi/8:
            out.append(2)
        elif bases[j] == pi/4:
            out.append(3)
        elif bases[j] == -pi/8:
            out.append(4)

    return out

def matchKeys(key1, key2, bases1, bases2):
    """Return the tuple (key1, key2, discard1, discard2) after removing bits where Alice
    and Bob selected incompatible axes of measurement in the E91 protocol.
    """
    match = [True if bases1[k] == bases2[k] else False for k in range(len(bases1))]
    discard1 = [key1[k] for k in range(len(key1)) if not(match[k])]
    key1 = [key1[k] for k in range(len(key1)) if match[k]]
    discard2 = [key2[k] for k in range(len(key2)) if not(match[k])]
    key2 = [not(key2[k]) for k in range(len(key2)) if match[k]]

    return (key1, key2, discard1, discard2)

def measureEntangledState(basisA, basisB, errorRate=0.0):
    """Return Alice and Bob's measurement results on a pair of maximally
    entangled qubits. basis[A,B] contain Alice and Bob's axes of mstment.
    """
    # Alice measures either basis state with equal probability
    # -1 will correspond to False (0) and +1 will correspond to True (1)
    resultA = random.choice([-1, 1])

    # If Alice and Bob chose the same axis of mstment, Bob's result is
    # perfectly anti-correlated with Alice's. Otherwise its correlation
    # coefficient is given by -cos[2(basisA-basisB)]. We use the result
    # r to generate a correlated random number that gives Bob's result.
    r = -1 * cos(2 * (basisA - basisB))
    r2 = r ** 2
    ve = 1 - r2
    SD = sqrt(ve)
    e = np.random.normal(0, SD)
    resultB = resultA * r + e

    resultA = False if resultA < 0 else True
    resultB = False if resultB < 0 else True

    if errorRate:
        samples = np.random.rand(2)
        if samples[0] < errorRate: resultA = not(resultA)
        if samples[1] < errorRate: resultB = not(resultB)

    return (resultA, resultB)
