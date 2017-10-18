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

## PRINT FUNCTIONS - where?
# TODO: this is a little awkward
def printStage0(numInitialBits, numTargetBits, eve, errorRate):
    # Initialization
    print("\n=====BB84 protocol=====\n%d initial bits, %d key bits" % (numInitialBits, numTargetBits))
    if eve: print("with eavesdropping")
    else: print("without eavesdropping")
    if errorRate: print("with channel noise")
    else: print("without channel noise")

def printStage1(numBits, rawKey, bases, verbose):
    # Raw key/basis generation
    print("\nAlice generates %d random bits as the raw key to be encoded:\n%s" % (numBits, util.bitFormat(rawKey)))
    print("For each bit, Alice randomly chooses one of two non-orthogonal sets of bases:\n%s" % util.bitFormat(bases))

    if verbose:
        print("\nAlice encodes each bit according to the following strategy:"\
              "\n    value | basis | state"\
              "\n      0   |   0   | +1 |0>"\
              "\n      0   |   1   | +0.7071 (|0> + |1>)"\
              "\n      1   |   0   | +1 |1>"\
              "\n      1   |   1   | +0.7071 (|0> - |1>)"\
              "\nShe then sends each qubit one by one to Bob over a quantum channel.\n")

def printStage2(numBits, bases_E, verbose):
    # Eavesdropping
    if verbose:
        print("Eve intercepts each qubit as it travels to Bob. Because it is not possible"\
                  "\nto clone quantum states, she must measure each qubit before re-sending to"\
                  "\nBob. Every time she measures a qubit in the 'wrong' basis, she has a 50%"\
                  "\nprobability of being detected.\n")

        print("Eve chooses a random basis to measure each qubit in:\n%s" % util.bitFormat(bases_E))

        if verbose: print("\nEve attempts to hide her actions by re-encoding her measurement result"\
                          "\nbefore re-sending the qubits to Bob.\n")

def printStage3(bases_B, key_B):
    # Bob's measurements
    print("Bob chooses a random basis to measure each qubit in:\n%s" % util.bitFormat(bases_B))
    print("Bob's measurement results:\n%s" % util.bitFormat(key_B))    

def printStage4(key_A, key_B, verbose):
    # Discard mismatches
    if verbose:
        print("\nBob announces when he has measured the last qubit and discloses"\
              "\nthe bases he used for each measurement. Alice and Bob then discard"\
              "\nany bits where they chose different bases.\n")

    print("Alice's key after discarding mismatches:\n%s" % util.bitFormat(key_A))
    print("Bob's key after discarding mismatches:\n%s" % util.bitFormat(key_B))        

def printStage5_1(numBits, announce_A, announce_B, verbose):
    # Sacrifice subset of keys
    if verbose:
        print("\nAlice and Bob sacrifice %d of their %d shared bits and publicly announce"\
              "\ntheir values. They agree to disclose every other bit of their shared key.\n" % (len(announce_A), numBits))

    print("Alice's announced bits:\n%s" % util.bitFormat(announce_A))
    print("Bob's announced bits:\n%s" % util.bitFormat(announce_B))

def printStage5_2(expectedError, actualError):
    # Error rate
    print("Expected error rate: %f" % expectedError)
    print("Actual error rate: %f" % actualError)

def printFinalKeys(numBits, key_A, key_B):
    # Compare final keys
    print("Alice's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_A)))
    print("Bob's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_B)))
