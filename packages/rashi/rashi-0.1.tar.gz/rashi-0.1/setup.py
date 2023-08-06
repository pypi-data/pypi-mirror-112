from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

VERSION = '0.1'
DESCRIPTION = 'Get Rashi'
LONG_DESCRIPTION = 'A simple package that scrapes out `rashi fals` from https: // www.hamropatro.com/rashifal'

# Setting up
setup(
    name="rashi",
    version=VERSION,
    author="Crain69 (Chirayu Prasai)",
    description=DESCRIPTION,
    author_email="<chirayuprasai11@gmail.com>",
    url="https://github.com/Crian69/rashi",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'nepali', 'rashi',
              'hamro', 'patro', 'horoscope'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ])
