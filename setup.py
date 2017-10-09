from setuptools import setup, find_packages

setup(name='qkdsim',
      version='1.0',
      description='Quantum Key Distribution Simulation Library',
      author='Conner Taylor',
      author_email='cmtaylor15@gmail.com',
      url='https://github.com/cotaylor/qkdsim',
      packages=find_packages(),
      install_requires=[
          'qit',
          'pycrypto'
          ]
      )
      
