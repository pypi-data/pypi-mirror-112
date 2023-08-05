from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='markupFor3DSlicer',
  version='0.2.1',
  description='Librairie de création de Markups pour 3D SLicer.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Guillaume ROCHE',
  author_email='g.roche1712@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='markup', 
  packages=find_packages(),
  install_requires=[''] 
)