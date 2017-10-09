import numpy as np
import qit
import qkdsim.qkdutils as util

def simulateNoise(bits, errorRate):
    """Simulate channel noise, each bit can be flipped with probability given by errorRate."""
    for k in range(len(bits)):
        p = np.random.random_sample()
        if p < errorRate:
            bits[k] = flipState(bits[k])

    return bits

def decodeState(state, basis):
    """Return a bool corresponding to the result of measuring the given state in the given basis."""
    # Change basis if necessary
    if basis:
        state = state.u_propagate(qit.H)

    _, result = state.measure()
    return bool(result)

def simulateEavesdrop(state, basis):
    """Measure an intercepted quantum state in the given basis, and attempt to hide the
    operation by re-encoding the measurement result in the same basis. Return the new state.
    """
    result = decodeState(state, basis)
    return encodeBit(result, basis)

def encodeBit(value, basis):
    """Return the quantum state representing the encoding of the given binary value in the given basis."""
    q = qit.state('0')

    if value:
        q = q.u_propagate(qit.sx) # Apply Pauli X operator to flip the qubit
    if basis:
        q = q.u_propagate(qit.H) # Apply Hadamard operator to change basis

    return q

def encodeKey(key, bases):
    """Return a list of quantum states corresponding to individual qubits prepared using the
    following encoding:
         key | bases | state
          0  |   0   | +1 |0>
          0  |   1   | +0.7071 |0> +0.7071 |1>
          1  |   0   | +1 |1>
          1  |   1   | +0.7071 |0> -0.7071 |1>
    key and bases are lists of bools representing binary values
    """
    # TODO: is this really necessary?
    if (len(key) != len(bases)):
        print("Invalid args: lists must be the same length")
        return -1

    encodedKey = []
    for k in range(len(key)):
        encodedKey.append(encodeBit(key[k], bases[k]))

    return encodedKey

def flipState(state):
    """Perform the transformation corresponding to a bit flip on the given quantum state
    and return it.
    """
    if util.equivState(state, qit.state('0')) or util.equivState(state, qit.state('1')):
        return state.u_propagate(qit.sx)
    else:
        return state.u_propagate(qit.sz)

def matchKeys(key1, key2, bases1, bases2):
    """If bases1[k] != bases2[k], discard bit k from both keys.
    Returns a tuple containing the resulting keys.
    """
    match = np.logical_not(np.logical_xor(bases1, bases2))
    newKey1 = [key1[k] for k in range(len(key1)) if match[k]]
    newKey2 = [key2[k] for k in range(len(key1)) if match[k]]
    return (newKey1, newKey2)
