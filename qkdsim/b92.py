import numpy as np
import qit
import qkdsim.qkdutils as util

def simulateNoise(bits, errorRate):
    """Simulate channel noise for the B92 protocol."""
    for k in range(len(bits)):
        p = np.random.random_sample()
        if p < errorRate: bits[k] = flipState(bits[k])

    return bits

def decodeState(state, basis):
    """Return a bool corresponding to the result of measuring the given state using one of two
    filters.
    If basis=0, the filter will pass antidiagonal photons and absorb diagonal photons.
    If basis=1, the filter will pass horizontal photons and absorb vertical photons.
    This corresponds to measuring the correct result 1/4 of the time, otherwise measuring nothing.
    """
    # Save the original bit Alice sent
    aliceBit = True
    if util.equivState(state, qit.state('0')):
        aliceBit = False

    # Apply chosen filter
    if basis == 0:
        state = state.u_propagate(qit.H)
    _, result = state.measure()

    if result:
        return aliceBit
    else:
        return None

def simulateEavesdrop(state, basis):
    result = decodeState(state, basis)
    if result != None:
        return encodeBit(result)

    return None

def encodeBit(value):
    """Return the quantum state representing the B92 encoding of the given binary value."""
    q = qit.state('0')
    if value:
        return q.u_propagate(qit.H)
    else:
        return q

def encodeKey(key):
    """Return a list of quantum states corresponding to the B92 encoding of the given binary string."""
    encodedKey = []
    for k in range(len(key)):
        encodedKey.append(encodeBit(key[k]))

    return encodedKey

def flipState(state):
    """Perform the transformation corresponding to a bit flip in the B92 protocol."""
    return state.u_propagate(qit.H)

def matchKeys(keyA, keyB):
    """Return the tuple (keyA, keyB) after removing bits where Bob's measured photon
    was absorbed. Assumes a value of -1 in keyB represents an absorbed photon.
    """
    match = [False if k == -1 else True for k in keyB]
    keyB = [keyB[k] for k in range(len(keyB)) if match[k]]

    while len(match) < len(keyA):
        match.append(True)
    keyA = [keyA[k] for k in range(len(keyA)) if match[k]]

    return (keyA, keyB)
