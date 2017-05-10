# qkd-simulation
Quantum Key Distribution simulation project for CSCI498: Introduction to Quantum Computing

Includes a survey and simulation of the BB84, B92, and E91 protocols for quantum key distribution, as well as solutions to selected exercises from Nielsen \& Chuang's _Quantum Computation and Quantum Information_.

## Files:
protocols.py - contains the simulations for BB84, B92, and E91.

qkdutils.py - contains function definitions required for the three protocols, including encoding/decoding, key matching, and random basis selection

qkdtests.py - contains a small number of unit tests to verify the correctness of the simulations

## Modules used:
NumPy - www.numpy.org

PyCrypto - https://www.dlitz.net/software/pycrypto

Quantum Information Toolkit (QIT) - qit.sourceforge.net

Nose - https://pypi.python.org/pypi/nose/1.3.7
