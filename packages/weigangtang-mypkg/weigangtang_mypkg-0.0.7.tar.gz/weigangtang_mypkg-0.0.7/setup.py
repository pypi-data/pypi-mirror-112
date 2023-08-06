from setuptools import setup, find_packages
from os import path
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent ',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

# full_path = path.abspath(path.dirname(__file__))
# with open(path.join(full_path, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read()
 
setup(
  name='weigangtang_mypkg',
  version='0.0.7',
  description='everyday functions for myself',
  long_description=long_description,
  long_description_content_type='text/markdown', 
  url='',  
  author='Weigang (Victor) Tang',
  author_email='tangw5@mcmaster.ca',
  license='MIT', 
  classifiers=classifiers,
  keywords='basic', 
  packages=find_packages(),
  install_requires=[] 
)