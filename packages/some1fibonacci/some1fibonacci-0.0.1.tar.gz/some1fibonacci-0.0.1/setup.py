"""
Your licence goes here
"""

from setuptools import setup, find_packages

# See note below for more information about classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='some1fibonacci',
    version='0.0.1',
    description='Fibonacci series program using function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Sneha',
    author_email='kawales543@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='fibonacci',
    packages=find_packages(),
    install_requires=['']
)
