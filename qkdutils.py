import numpy as np
import qit


def addNoiseB92(bits, errorRate):
    """Simulate channel noise for the B92 protocol."""
    for k in range(len(bits)):
        p = np.random.random_sample()
        if p < errorRate: bits[k] = flipStateB92(bits[k])

    return bits


def addNoiseBB84(bits, errorRate):
    """Simulate channel noise, each bit can be flipped with probability given by errorRate."""
    for k in range(len(bits)):
        p = np.random.random_sample()
        if p < errorRate: bits[k] = flipStateBB84(bits[k])

    return bits

def bitFormat(bits):
    """Return a printable representation of the given list of bools representing bits."""
    return '[' + ', '.join(['1' if b == True else '0' if b == False else '-' for b in bits]) + ']'


def decodeStateB92(state, basis):
    """Return a bool corresponding to the result of measuring the given state using one of two
    filters.
    If basis=0, the filter will pass antidiagonal photons and absorb diagonal photons.
    If basis=1, the filter will pass horizontal photons and absorb vertical photons.
    This corresponds to measuring the correct result 1/4 of the time, otherwise measuring nothing.
    """
    # Save the original bit Alice sent
    aliceBit = True
    if equivState(state, qit.state('0')): aliceBit = False

    # Apply chosen filter
    if basis == 0: state = state.u_propagate(qit.H)

    _, result = state.measure()
    if result:
        return aliceBit
    else:
        return None


def decodeStateBB84(state, basis):
    """Return a bool corresponding to the result of measuring the given state in the given basis."""
    # Change basis if necessary
    if basis: state = state.u_propagate(qit.H)

    # Measure in the chosen basis
    _, result = state.measure()

    return bool(result)


def detectEavesdrop(key1, key2, errorRate):
    """Return True if Alice and Bob detect Eve's interference, False otherwise."""
    if len(key1) == 0 or len(key2) == 0: return True

    tolerance = errorRate * 1.2
    if len(key1) != len(key2): return True
    mismatch = sum([1 for k in range(len(key1)) if key1[k] != key2[k]])
    print("actual error: %f, expected error: %f") % (abs(float(mismatch)/len(key1) - errorRate), tolerance)
    if abs(float(mismatch)/len(key1) - errorRate) > tolerance: return True

    return False


def decodeStateE91(state):
    # TODO: implement
    return None


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


def eavesdropB92(state, basis):
    result = decodeStateB92(state, basis)
    if result != None: return encodeBitB92(result)

    return None


def eavesdropBB84(state, basis):
    """Measure an intercepted quantum state in the given basis, and attempt to hide the
    operation by re-encoding the measurement result in the same basis. Return the new state.
    """
    result = decodeStateBB84(state, basis)
    return encodeBitBB84(result, basis)


def encodeBitB92(value):
    """Return the quantum state representing the B92 encoding of the given binary value."""
    q = qit.state('0')
    if value:
        return q.u_propagate(qit.H)
    else:
        return q


def encodeBitBB84(value, basis):
    """Return the quantum state representing the encoding of the given binary value in the given basis."""
    q = qit.state('0')
    if value: q = q.u_propagate(qit.sx)    # Apply Pauli X operator to flip bit
    if basis: q = q.u_propagate(qit.H)    # Apply Hadamard operator to change basis

    return q


def encodeKeyB92(key):
    """Return a list of quantum states corresponding to the B92 encoding of the given binary string."""
    qs = []
    for k in range(len(key)):
        qs.append(encodeBitB92(key[k]))

    return qs


def encodeKeyBB84(key, bases):
    """Return a list of quantum states corresponding to individual qubits prepared using the
    following encoding:
         key | bases | state
          0  |   0   | +1 |0>
          0  |   1   | +0.7071 |0> +0.7071 |1>
          1  |   0   | +1 |1>
          1  |   1   | +0.7071 |0> -0.7071 |1>
    key and bases are lists of bools representing binary values
    """
    if (len(key) != len(bases)):
        print("Invalid args: lists must be the same length")
        return -1

    # Encode each bit in the chosen basis
    qs = []
    for k in range(len(key)):
        qs.append(encodeBitBB84(key[k], bases[k]))
    return qs


def equivState(q1, q2):
    """Return True if q1 and q2 represent the same quantum state."""
    return np.array_equal(q1.prob(), q2.prob())


def flipStateB92(q):
    """Perform the transformation corresponding to a bit flip in the B92 protocol."""
    return q.u_propagate(qit.H)


def flipStateBB84(q):
    """Perform the transformation corresponding to a bit flip on the given quantum state
    and return it. TODO: is there a better way to simulate noise?
    """
    if equivState(q, qit.state('0')) or equivState(q, qit.state('1')):
        return q.u_propagate(qit.sx)
    else:
        return q.u_propagate(qit.sz)


def getRandomBits(n):
    """Return a list of n bits, each either 0 or 1 with equal probability."""
    dist = np.random.rand(n)
    bitstring = [elem > 0.5 for elem in dist]
    return bitstring


def matchKeysBB84(key1, key2, bases1, bases2):
    """If bases1[k] != bases2[k], discard bit k from both keys.
    Returns a tuple containing the resulting keys.
    """
    match = np.logical_not(np.logical_xor(bases1, bases2))
    newKey1 = [key1[k] for k in range(len(key1)) if match[k]]
    newKey2 = [key2[k] for k in range(len(key1)) if match[k]]

    return (newKey1, newKey2)


def matchKeysB92(key_A, key_B):
    """Return the tuple (key_A, key_B) after removing bits where Bob's measured photon
    was absorbed. Assumes a value of -1 in key_B represents an absorbed photon.
    """
    match = [False if elem == -1 else True for elem in key_B]
    key_B = [key_B[elem] for elem in range(len(key_B)) if match[elem]]

    while len(match) < len(key_A):
        match.append(True)
    key_A = [key_A[elem] for elem in range(len(key_A)) if match[elem]]

    return (key_A, key_B)
