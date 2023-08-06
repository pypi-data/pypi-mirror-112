from setuptools import setup

setup(
   name='mehr',
   version='0.0.1',
   author='Moraxno',
   author_email='robertbock.98@googlemail.com',
   packages=['mehr'],
   scripts=[],
   url='http://pypi.python.org/pypi/mehr/',
   license='LICENSE.txt',
   description='Helpers',
   long_description=open('README.md').read(),
   download_url='https://github.com/Moraxno/py-mehr/archive/refs/tags/v0.0.1.tar.gz',
   install_requires=[
       "pytest",
   ],
   classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)