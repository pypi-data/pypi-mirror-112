from setuptools import setup, find_packages
 
#'Intended Audience :: Education',
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='LibForShiva',
  version='1.0.1',
  description='Librairie de simplification pour Shiva.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Guillaume ROCHE',
  author_email='g.roche1712@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Shiva', 
  packages=find_packages(),
  install_requires=[''] 
)