from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Jarve',
  version='0.0.3',
  description='A module for A.I',
  long_description=open('README.md').read(),
  url='',  
  author='Kittex0/Mohammed Daniyal',
  author_email='kittex0@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='A.I', 
  packages=find_packages(),
  install_requires=[''] 
)