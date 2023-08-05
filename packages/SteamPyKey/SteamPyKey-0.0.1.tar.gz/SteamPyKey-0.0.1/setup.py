from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SteamPyKey',
  version='0.0.1',
  description='Very simple library to make random keys in canvas like steam does!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Piotr Kobylorz',
  author_email='kacper@horsefucker.org',
  license='MIT', 
  classifiers=classifiers,
  keywords='steam',
  packages=find_packages(),
  install_requires=['random', 'string'] 
)