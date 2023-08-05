from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cspyclient',
  version='1.0.0', 
  description='An internal tool to work with CoderSchool Backend API',
  author='Minh Hai Do',
  author_email='minhdh@coderschool.vn',
  license='MIT', 
  classifiers=classifiers,
  packages=['cspyclient'],
  install_requires=['pandas', 'requests'],
  tests_require=['pytest']
)