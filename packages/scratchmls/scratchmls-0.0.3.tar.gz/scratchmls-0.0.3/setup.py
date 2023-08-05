from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='scratchmls',
  version='0.0.3',
  description='Custom Python library for Machine Learning',
  url='',  
  author='Faraz Khan',
  author_email='farazkhan138@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='MachineLearning', 
  packages=find_packages(),
  install_requires=['numpy'] 
)