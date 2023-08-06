
from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='trading_com_dados',
    version='0.0.2',
    license='MIT License',
    author='Fabio Minutti Teixeira',
    long_description=readme,
    author_email='fabiomt92@hotmail.com',
    keywords='',
    description='Pacote trading com dados teste',
    packages=['trading_com_dados'],
    install_requires=[],)

        