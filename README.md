# qkd-simulation
Quantum Key Distribution simulation project for CSCI498: Introduction to Quantum Computing

Includes a survey and simulation of the BB84, B92, and E91 protocols for quantum key distribution, as well as solutions to selected exercises from Nielsen \& Chuang's _Quantum Computation and Quantum Information_.

## Installation
```bash
pip install -r requirements.txt
python setup.py install
```

## Example Usage
```python
import qkdsim.simulations as sim
sim.runBB84(<keylen>)
```

## Modules used:
NumPy - www.numpy.org

PyCrypto - https://www.dlitz.net/software/pycrypto

Quantum Information Toolkit (QIT) - qit.sourceforge.net

Nose - https://pypi.python.org/pypi/nose/1.3.7
