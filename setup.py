from setuptools import setup, find_packages


# Dynamically calculate the version based on jsonrpc.VERSION
version = '.'.join([str(v) for v in __import__('pycard').VERSION])

setup(
    name='pycard',
    description='A simple Python library for credit card validation',
    version=version,
    author='Michael Angeletti',
    author_email='michael [at] angelettigroup [dot] com',
    url='http://github.com/orokusaki/py-card/',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    packages=find_packages(),
)
