import qkdutils as util
from math import pi
import qit
import numpy as np
import protocols
import bb84, b92, e91

def test_runBB84():
    numTrials = 20
    numBits = 2048

    for j in range(numTrials):
        assert(len(simulations.runBB84(numBits, False, 0.0, False)) >= 3*numBits/4)
        assert(simulations.runBB84(numBits, True, 0.0, False) == -1)


def test_simulateB92():
    numTrials = 20
    numBits = 2048

    for j in range(numTrials):
        assert(len(simulations.runB92(numBits, False, 0.0, False)) >= 3*numBits/4)
        assert(simulations.runB92(numBits, True, 0.0, False) == -1)


def test_decodeStateB92():
    # Test probabilistic results match our expectations:
    # If sent == basis, measure the value of sent 50% of the time
    # If sent not measured, nothing comes through the filter
    numTrials = 50
    numBits = 1024
    sent = util.getRandomBits(numBits)
    bases = util.getRandomBits(numBits)
    tolerance = 0.05

    for j in range(numTrials):
        seen = 0

        for k in range(numBits):
            q = qit.state('0')
            if sent[k]: q = q.u_propagate(qit.H)

            result = b92.decodeState(q, bases[k])
            if result != None:
                seen += 1
                assert(result == sent[k])

        # Expect to get ~1/4 of the original key material
        print(float(seen)/numBits)
        assert(abs(float(seen)/numBits - 0.25) < tolerance)


def test_decodeStateBB84_deterministic():
    # Test deterministic cases
    q = qit.state('0')
    assert(bb84.decodeState(q, 0) == False)
    q = q.u_propagate(qit.H)
    assert(bb84.decodeState(q, 1) == False)
    q  = qit.state('1')
    assert(bb84.decodeState(q, 0) == True)
    q = q.u_propagate(qit.H)
    assert(bb84.decodeState(q, 1) == True)


def test_decodeStateBB84_probabilistic():
    # Test probabilistic measurement is roughly even
    numTrials = 10000
    tolerance = 0.1 * numTrials

    q = qit.state('0')
    counts = [0, 0]
    for j in range(numTrials):
        counts[bb84.decodeState(q, 1)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[bb84.decodeState(q, 0)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)

    q = qit.state('1')
    counts = [0, 0]
    for j in range(numTrials):
        counts[bb84.decodeState(q, 1)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[bb84.decodeState(q, 0)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)


def test_discloseHalf():
    numTrials = 128

    for j in range(numTrials):
        key1 = util.getRandomBits(j)
        key2 = util.getRandomBits(j)
        announce1, key1, announce2, key2 = util.discloseHalf(key1, key2)
        assert(len(key1) + len(announce1) == j)
        assert(len(key2) + len(announce2) == j)


def test_simulateE91():
    numTrials = 20
    numBits = 2048

    for j in range(numTrials):
        assert(len(simulations.runE91(numBits)) >= 3*numBits/4)


def test_encodeBitBB84():
    # Only test the 4 cases in our encoding strategy
    assert(util.equivState(bb84.encodeBit(0,0), qit.state('0')))
    assert(util.equivState(bb84.encodeBit(1,0), qit.state('1')))
    assert(util.equivState(bb84.encodeBit(0,1), qit.state('0').u_propagate(qit.H)))
    assert(util.equivState(bb84.encodeBit(1,1), qit.state('1').u_propagate(qit.H)))


def test_getRandomBits():
    counts = [0, 0]
    numBits = 1024
    numTrials = 100
    tolerance = 0.1 * numBits

    for j in range(numTrials):
        bits = util.getRandomBits(numBits)
        counts[0] = len([j for j in bits if j==0])
        counts[1] = len([j for j in bits if j==1])
        print(abs(counts[0]-counts[1]))
        assert(abs(counts[0]-counts[1]) < tolerance)


def test_matchKeysBB84():
    numTrials = 100
    numBits = 256

    for j in range(numTrials):
        key1 = util.getRandomBits(numBits)
        bases1 = util.getRandomBits(numBits)
        sent = bb84.encodeKey(key1, bases1)
        bases2 = util.getRandomBits(numBits)
        key2 = []
        for k in range(numBits):
            key2.append(bb84.decodeState(sent[k], bases2[k]))

        result1, result2 = bb84.matchKeys(key1, key2, bases1, bases2)
        assert(result1 == result2)


def test_measureEntangledState():
    numTrials = 10000

    for j in range(numTrials):
        (basisA, basisB) = e91.chooseAxes(1)
        (A, B) = e91.measureEntangledState(basisA[0], basisB[0])
        if basisA == basisB:
            assert(A != B)    # Bob's result must be anti-correlated with Alice's
