from distutils.core import setup
from pip.req import parse_requirements

setup(name='qkdsim',
      version='1.0',
      description='Quantum Key Distribution Simulation Library',
      author='Conner Taylor',
      author_email='cmtaylor15@gmail.com',
      url='https://github.com/cotaylor/qkdsim',
      packages=['qkdsim'],
      install_requires=[
          'qit',
          'pycrypto'
          ]
      )
      
