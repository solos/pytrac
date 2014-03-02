
#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append('./src')

from distutils.core import setup
from pytrac import __version__

setup(name='pytrac',
      version=__version__,
      description='A python empty project',
      long_description=open('README.md').read(),
      author='solos',
      author_email='solos@solos.so',
      packages=['pytrac'],
      package_dir={'pytrac': 'src/pytrac'},
      package_data={'pytrac': ['stuff']},
      license='MIT',
      platforms=['any'],
      url='https://github.com/solos/pytrac')
