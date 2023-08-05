from setuptools import setup, find_packages

VERSION = '0.1.7'
DESCRIPTION = 'Tracks and analyzes the performance of stocks'
LONG_DESCRIPTION = 'Tracks and analyzes the performance of stocks'
# Setting up
setup(
    name="stock-wizard",
    version=VERSION,
    author="Hailu Teju",
    author_email="hailuteju@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where='stock-tracker-app'),
    install_requires=['pandas>=1.3.0',
                      'plotly>=5.1.0',
                      'matplotlib>=3.4.2',
                      'yfinance>=0.1.60'],
    keywords=['python', 'stock', 'stock tracker', 'bollinger bands'],
    zip_safe=False
)
