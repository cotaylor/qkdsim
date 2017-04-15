from utils import *
import qit
import numpy as np

def test_decodeState_deterministic():
    # Test deterministic cases
    q = qit.state('0')
    assert decodeState(q, 0) == False
    q = q.u_propagate(qit.H)
    assert decodeState(q, 1) == False
    q  = qit.state('1')
    assert decodeState(q, 0) == True
    q = q.u_propagate(qit.H)
    assert decodeState(q, 1) == True

def test_decodeState_probabilistic():
    # Test probabilistic measurement is roughly even
    numTrials = 1000
    tolerance = 0.1 * numTrials
    
    q = qit.state('0')
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeState(q, 1)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeState(q, 0)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

    q = qit.state('1')
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeState(q, 1)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

    q = q.u_propagate(qit.H)
    counts = [0, 0]
    for j in range(numTrials):
        counts[decodeState(q, 0)] += 1
    assert abs(counts[0] - counts[1]) < tolerance

def test_encodeBit():
    # Only test the 4 cases in our encoding strategy
    assert(equivState(encodeBit(0,0), qit.state('0')))
    assert(equivState(encodeBit(1,0), qit.state('1')))
    assert(equivState(encodeBit(0,1), qit.state('0').u_propagate(qit.H)))
    assert(equivState(encodeBit(1,1), qit.state('1').u_propagate(qit.H)))

def test_getRandomBits():
    counts = [0, 0]
    numBits = 1024
    numTrials = 50
    tolerance = 0.1 * numBits

    for j in range(numTrials):
        bits = getRandomBits(numBits)
        counts[0] = len([j for j in bits if j==0])
        counts[1] = len([j for j in bits if j==1])
        print(counts[0], counts[1])
        assert(abs(counts[0]-counts[1]) < tolerance)

def test_matchKeys():
    numTrials = 50
    numBits = 256

    for j in range(numTrials):
        key1 = getRandomBits(numBits)
        bases1 = getRandomBits(numBits)
        sent = encodeRawKey(key1, bases1)
        bases2 = getRandomBits(numBits)
        key2 = []
        for k in range(numBits):
            key2.append(decodeState(sent[k], bases2[k]))
            
        result1, result2 = matchKeys(key1, key2, bases1, bases2)
        assert(result1 == result2)


    
    

