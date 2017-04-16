import numpy as np
import qit

def bitFormat(bits):
    """Return a printable representation of the given list of bools."""
    return '[' + ', '.join(['1' if elem else '0' for elem in bits]) + ']'


def decodeState(state, basis):
    """Return a bool corresponding to the result of measuring the given state in the given basis."""
    # Change basis if necessary
    if basis: state = state.u_propagate(qit.H)

    # Measure in the chosen basis
    _, result = state.measure()
    
    return bool(result)


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

    
def eavesdrop(state, basis):
    """Measure an intercepted quantum state in the given basis, and attempt to hide the
    operation by re-encoding the measurement result in the same basis. Return the new state.
    """
    result = decodeState(state, basis)
    newState = encodeBit(result, basis)

    return newState


def encodeBit(value, basis):
    """Return the quantum state representing the encoding of the given binary value in the given basis"""
    q = qit.state('0')
    if value: q = q.u_propagate(qit.sx)    # Apply Pauli X operator to flip bit
    if basis: q = q.u_propagate(qit.H)    # Apply Hadamard operator to change basis

    return q
        

def encodeRawKey(key, bases):
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
        qs.append(encodeBit(key[k], bases[k]))
    return qs


def equivState(q1, q2):
    """Return True if q1 and q2 represent the same quantum state."""
    return np.array_equal(q1.prob(), q2.prob())


def flipState(q):
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


def matchKeys(key1, key2, bases1, bases2):
    """If bases1[k] != bases2[k], discard bit k from both keys.
    Returns a tuple containing the resulting keys.
    """
    match = np.logical_not(np.logical_xor(bases1, bases2))
    newKey1 = [key1[k] for k in range(len(key1)) if match[k]]
    newKey2 = [key2[k] for k in range(len(key1)) if match[k]]

    return (newKey1, newKey2)
