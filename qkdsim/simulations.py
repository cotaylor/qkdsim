import qkdsim.bb84 as bb84
import qkdsim.b92 as b92
import qkdsim.e91 as e91
import qkdsim.qkdutils as util

def runBB84(n, eve=False, errorRate=0.0, verbose=True):
    """Simulation of Bennett & Brassard's 1984 protocol for quantum key distribution with
    n initial bits in the raw key.
    If eve is set to True, assumes the presence of an eavesdropper attempting an
    intercept-resend attack.
    """
    numBits = 5 * n

    if verbose:
        print("\n=====BB84 protocol=====\n%d initial bits, ~%d key bits" % (numBits, n))
        if eve: print("with eavesdropping")
        else: print("without eavesdropping")
        if errorRate: print("with channel noise")
        else: print("without channel noise")

    # Alice generates a random bit string to be encoded
    rawKey = util.getRandomBits(numBits)

    # Alice also randomly chooses which basis to use when encoding each bit
    # 0: computational basis; 1: Hadamard basis
    bases_A = util.getRandomBits(numBits)

    print("\nAlice generates %d random bits to be encoded:\n%s" % (numBits, util.bitFormat(rawKey)))
    print("For each bit, Alice randomly chooses one of two non-orthogonal sets of bases:\n%s" % util.bitFormat(bases_A))

    if verbose:
        print("\nAlice encodes each bit according to the following strategy:"\
              "\n    value | basis | state"\
              "\n      0   |   0   | +1 |0>"\
              "\n      0   |   1   | +0.7071 (|0> + |1>)"\
              "\n      1   |   0   | +1 |1>"\
              "\n      1   |   1   | +0.7071 (|0> - |1>)"\
              "\nShe then sends each qubit one by one to Bob over a quantum channel.\n")

    # Alice prepares n qubits, with the kth qubit in state |0> or |1> in either the computational
    # basis or the Hadamard basis, depending on the value of the kth bit in each bitstring
    sent_A = bb84.encodeKey(rawKey, bases_A)

    # QKD guarantees with high probability we will detect any eavesdropping

    if eve:
        if verbose:
            print("Eve intercepts each qubit as it travels to Bob. Because it is not possible"\
                  "\nto clone quantum states, she must measure each qubit before re-sending to"\
                  "\nBob. Every time she measures a qubit in the 'wrong' basis, she has a 50%"\
                  "\nprobability of being detected.\n")

        # No matter what strategy Eve uses to select bases, the probability she will be detected
        # is always 1-(3/4)^numBits if Alice chose her bases randomly
        bases_E = util.getRandomBits(numBits)
        print("Eve chooses a random basis to measure each qubit in:\n%s" % util.bitFormat(bases_E))

        # Eve measures each qubit and attempts to cover her tracks
        for k in range(numBits):
            sent_A[k] = bb84.simulateEavesdrop(sent_A[k], bases_E[k])

        if verbose: print("\nEve attempts to hide her actions by re-encoding her measurement result"\
                          "\nbefore re-sending the qubits to Bob.\n")

    # Introduce error due to noise
    sent_A = bb84.simulateNoise(sent_A, errorRate)

    # Bob measures each qubit in a randomly chosen basis
    bases_B = util.getRandomBits(numBits)
    key_B = []
    for k in range(numBits):
        key_B.append(bb84.decodeState(sent_A[k], bases_B[k]))

    print("Bob chooses a random basis to measure each qubit in:\n%s" % util.bitFormat(bases_B))
    print("Bob's measurement results:\n%s" % util.bitFormat(key_B))

    # Alice and Bob discard any bits where they chose different bases.
    key_A, key_B = bb84.matchKeys(rawKey, key_B, bases_A, bases_B)
    numBits = len(key_A)

    if verbose:
        print("\nBob announces when he has measured the last qubit and discloses"\
              "\nthe bases he used for each measurement. Alice and Bob then discard"\
              "\nany bits where they chose different bases.\n")

    print("Alice's key after discarding mismatches:\n%s" % util.bitFormat(key_A))
    print("Bob's key after discarding mismatches:\n%s" % util.bitFormat(key_B))

    # Alice and Bob sacrifice a subset of their bits to try to detect Eve
    announce_A, key_A, announce_B, key_B = util.discloseHalf(key_A, key_B)
    if verbose:
        print("\nAlice and Bob sacrifice %d of their %d shared bits and publicly announce"\
              "\ntheir values. They agree to disclose every other bit of their shared key.\n" % (len(announce_A), numBits))

    print("Alice's announced bits:\n%s" % util.bitFormat(announce_A))
    print("Bob's announced bits:\n%s" % util.bitFormat(announce_B))

    numBits = len(key_A)
    print("Alice's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_A)))
    print("Bob's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_B)))

    print("Expected error rate: %f" % errorRate)
    print("Actual error rate: %f" % (float(sum([1 for k in range(len(key_A)) if key_A[k] != key_B[k]]))/len(key_A)))

    if util.detectEavesdrop(key_A, key_B, errorRate):
        print("\nAlice and Bob detect Eve's interference and abort the protocol.")
        return -1

    return key_A

def runB92(n, eve=False, errorRate=0.0, verbose=True):
    """Simulation of Bennet's 1992 protocol for quantum key distribution with n initial
    bits in the raw key. If eve is set to True, assumes the presence of an eavesdropper
    attempting an intercept-resend attack. errorRate represents the probability that a bit
    will be flipped when Bob measures it.
    """

    numBits = 8 * n

    if verbose:
        print("\n=====B92 protocol=====\n%d initial bits, ~%d key bits" % (numBits, n))
        if eve: print("with eavesdropping")
        else: print("without eavesdropping")
        if errorRate: print("with channel noise")
        else: print("without channel noise")

    # Alice generates a random bit string to be encoded
    rawKey = util.getRandomBits(numBits)
    print("\nAlice generates %d random bits to be encoded:\n%s" % (numBits, util.bitFormat(rawKey)))

    # Alice encodes each bit as a qubit as |0> in either the computational or Hadamard basis
    sent_A = b92.encodeKey(rawKey)
    if verbose:
        print("Alice encodes each bit according to the following strategy:"\
          "\n    value | state"\
          "\n      0   | +1 |0>"\
          "\n      1   | +0.7071 (|0> + |1>)"\
          "\nShe then sends each qubit one by one to Bob over a quantum channel.\n")

    # QKD guarantees with high probability we will detect any eavesdropping
    if eve:
        if verbose:
            print("Eve intercepts each qubit as it travels to Bob. Because it is not possible"\
                  "\nto clone quantum states, she must measure each qubit before re-sending to Bob.\n")

        # Eve randomly selects a filter to use for each qubit
        bases_E = util.getRandomBits(numBits)
        print("Eve chooses a random filter to measure each qubit with:\n%s" % util.bitFormat(bases_E))

        # Eve measures each qubit and attempts to cover her tracks
        temp = []
        for k in range(numBits):
            result = b92.simulateEavesdrop(sent_A[k], bases_E[k])
            if result != None: temp.append(result)

        sent_A = temp
        numBits = len(sent_A)

        if verbose: print("\nEve attempts to hide her actions by re-encoding her measurement result"\
                          "\nbefore re-sending the qubits to Bob.\n")

    # Introduce error due to noise
    sent_A = b92.simulateNoise(sent_A, errorRate)

    # Bob measures each qubit in a randomly chosen basis
    bases_B = util.getRandomBits(numBits)
    key_B = []
    for k in range(numBits):
        result = b92.decodeState(sent_A[k], bases_B[k])
        if result == None: key_B.append(-1)
        else: key_B.append(result)

    print("Bob chooses a random filter to measure each qubit with:\n%s" % util.bitFormat(bases_B))
    print("Bob's measurement results:\n%s" % util.bitFormat(key_B))

    # Discard bits where Bob did not see a result
    key_A, key_B = b92.matchKeys(rawKey, key_B)
    numBits = len(key_B)

    if verbose:
        print("\nBob announces which photons were completely absorbed and"\
          "\nAlice and Bob discard the corresponding bits from their keys.\n")
    print("Alice's sifted key:\n%s" % util.bitFormat(key_A))
    print("Bob's sifted key:\n%s" % util.bitFormat(key_B))

    # Compare key information
    if len(key_A) != len(key_B):
        print("\nAlice and Bob announce the lengths of their keys. Since Alice's"\
              "\nkey is %d bits and Bob's is %d bits, they are able to detect"\
              "\nEve's interference and abort the protocol.\n" % (len(key_A), len(key_B)))
        return -1

    announce_A, key_A, announce_B, key_B = util.discloseHalf(key_A, key_B)
    if verbose:
        print("\nAlice and Bob sacrifice %d of their %d shared bits and publicly announce"\
              "\ntheir values. They agree to disclose every other bit of their shared key.\n" % (len(announce_A), numBits))
    print("Alice's announced bits:\n%s" % util.bitFormat(announce_A))
    print("Bob's announced bits:\n%s" % util.bitFormat(announce_B))

    numBits = len(key_A)
    print("Alice's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_A)))
    print("Bob's remaining %d-bit key:\n%s" % (numBits, util.bitFormat(key_B)))

    print("Expected error rate: %f" % errorRate)
    print("Actual error rate: %f" % (float(sum([1 for k in range(len(key_A)) if key_A[k] != key_B[k]]))/len(key_A)))

    if util.detectEavesdrop(key_A, key_B, errorRate):
        print("\nAlice and Bob detect Eve's interference and abort the protocol.\n")
        return -1

    return key_A

def runE91(n, errorRate=0.0, verbose=True):
    """Simulation of Ekert's 1991 entanglement-based protocol for quantum key distribution."""
    numBits = 5 * n

    if verbose:
        print("\n=====E91 protocol=====\n%d initial bits, ~%d key bits" % (numBits, n))
        print("without eavesdropping")
        if errorRate: print("with channel noise\n")
        else: print("without channel noise\n")

    # A trusted mediator generates pairs of particles in the singlet state
    #     +0.7071 |0> -0.7071 |1>
    # and sends one particle from each pair to Alice and the other to Bob.
    # Alice randomly offsets her axis of measurement by one of the following:
    #     [0, pi/8, pi/4]
    # Bob randomly offsets his axis of measurement by one of the following:
    #     [0, pi/8, -pi/8]
    bases_A, bases_B = e91.chooseAxes(numBits)
    key_A, key_B = [], []

    for j in range(numBits):
        (new_A, new_B) = e91.measureEntangledState(bases_A[j], bases_B[j], errorRate)
        key_A.append(new_A)
        key_B.append(new_B)

    print("Alice's randomly chosen axes of measurement:\n%s" % e91.formatBasesForPrint(bases_A))
    print("Bob's randomly chosen axes of measurement:\n%s" % e91.formatBasesForPrint(bases_B))
    print("Alice's measurement results:\n%s" % util.bitFormat(key_A))
    print("Bob's measurement results:\n%s" % util.bitFormat(key_B))

    key_A, key_B, discard_A, discard_B = e91.matchKeys(key_A, key_B, bases_A, bases_B)
    print("Alice's %d discarded bits:\n%s" % (len(discard_A), util.bitFormat(discard_A)))
    print("Bob's %d discarded bits:\n%s" % (len(discard_B), util.bitFormat(discard_B)))

    print("Alice's %d-bit sifted key:\n%s" % (len(key_A), util.bitFormat(key_A)))
    print("Bob's %d-bit sifted key:\n%s" % (len(key_B), util.bitFormat(key_B)))

    return key_A
