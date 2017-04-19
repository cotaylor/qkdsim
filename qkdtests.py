from qkdutils import *
import qit
import numpy as np


def test_decodeStateB92():
    # Test probabilistic results match our expectations:
    # If sent == basis, measure the value of sent 50% of the time
    # If sent not measured, nothing comes through the filter
    numTrials = 30
    numBits = 1024
    sent = getRandomBits(numBits)
    bases = getRandomBits(numBits)
    tolerance = 0.05

    for j in range(numTrials):
        seen = 0

        for k in range(numBits):
            q = qit.state('0')
            if sent[k]: q = q.u_propagate(qit.H)

            result = decodeStateB92(q, bases[k])
            if result != None:
                seen += 1
                assert(result == sent[k])

        # Expect to get ~1/4 of the original key material
        print(float(seen)/numBits)
        assert(abs(float(seen)/numBits - 0.25) < tolerance)


def test_decodeStateBB84_deterministic():
    # Test deterministic cases
    q = qit.state('0')
    assert(decodeStateBB84(q, 0) == False)
    q = q.u_propagate(qit.H)
    assert(decodeStateBB84(q, 1) == False)
    q  = qit.state('1')
    assert(decodeStateBB84(q, 0) == True)
    q = q.u_propagate(qit.H)
    assert(decodeStateBB84(q, 1) == True)


def test_decodeStateBB84_probabilistic():
    # Test probabilistic measurement is roughly even
    numTrials = 1000
    tolerance = 0.1 * numTrials

    q = qit.state('0')
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeStateBB84(q, 1)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeStateBB84(q, 0)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)

    q = qit.state('1')
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeStateBB84(q, 1)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeStateBB84(q, 0)] += 1
    assert(abs(counts[0] - counts[1]) < tolerance)


def test_discloseHalf():
    numTrials = 1024

    for j in range(numTrials):
        key1 = getRandomBits(j)
        key2 = getRandomBits(j)
        announce1, key1, announce2, key2 = discloseHalf(key1, key2)
        assert(len(key1) + len(announce1) == j)
        assert(len(key2) + len(announce2) == j)


def test_encodeBitBB84():
    # Only test the 4 cases in our encoding strategy
    assert(equivState(encodeBitBB84(0,0), qit.state('0')))
    assert(equivState(encodeBitBB84(1,0), qit.state('1')))
    assert(equivState(encodeBitBB84(0,1), qit.state('0').u_propagate(qit.H)))
    assert(equivState(encodeBitBB84(1,1), qit.state('1').u_propagate(qit.H)))


def test_getRandomBits():
    counts = [0, 0]
    numBits = 1024
    numTrials = 50
    tolerance = 0.1 * numBits

    for j in range(numTrials):
        bits = getRandomBits(numBits)
        counts[0] = len([j for j in bits if j==0])
        counts[1] = len([j for j in bits if j==1])
        print(abs(counts[0]-counts[1]))
        assert(abs(counts[0]-counts[1]) < tolerance)


def test_matchKeys():
    numTrials = 50
    numBits = 256

    for j in range(numTrials):
        key1 = getRandomBits(numBits)
        bases1 = getRandomBits(numBits)
        sent = encodeKeyBB84(key1, bases1)
        bases2 = getRandomBits(numBits)
        key2 = []
        for k in range(numBits):
            key2.append(decodeStateBB84(sent[k], bases2[k]))

        result1, result2 = matchKeys(key1, key2, bases1, bases2)
        assert(result1 == result2)
