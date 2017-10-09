from distutils.core import setup
from pip.req import parse_requirements

# get requirements for install_requires
install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(name='qkdsim',
      version='1.0',
      description='Quantum Key Distribution Simulation Library',
      author='Conner Taylor',
      author_email='cmtaylor15@gmail.com',
      url='https://github.com/cotaylor/qkdsim',
      packages=['qkdsim'],
      install_requires=reqs
      )
      
