import numpy as np
import qit

def decodeState(state, basis):
    """Return a bool corresponding to the result of measuring the given state in the given basis."""
    # Change basis if necessary
    if basis: state.u_propagate(qit.H)

    # Measure in the chosen basis
    _, result = state.measure()
    
    return bool(result)

def encodeRawKey(key, bases):
    """Return a list of quantum states corresponding to individual qubits prepared using the
    following encoding:
         key | bases | state
          0  |   0   | |0>
          0  |   1   | 0.5|0> + 0.5|1>
          1  |   0   | |1>
          1  |   1   | 0.5|0> - 0.5|1>

    key and bases are lists of bools representing binary values
    """
    if (len(key) != len(bases)):
        print("Invalid args: lists must be the same length")
        return -1
    
    template = qit.state("0")
    qs = []
    for k in range(len(key)):
        # Create a new qubit in state |0>
        qk = template

        # Apply encoding
        if key[k]: qk = qk.u_propagate(qit.sx)    # apply Pauli X operator to flip bit
        if bases[k]: qk = qk.u_propagate(qit.H)    # apply Hadamard operator to change basis

        qs.append(qk)
        
    return qs

def getRandomBits(n):
    """Return a list of n bits, each either 0 or 1 with equal probability."""
    dist = np.random.rand(n)
    bitstring = [elem > 0.5 for elem in dist]
    return bitstring

def bitFormat(bits):
    """Return a printable representation of the given list of bools."""
    return '[' + ', '.join(['1' if elem else '0' for elem in bits]) + ']'
