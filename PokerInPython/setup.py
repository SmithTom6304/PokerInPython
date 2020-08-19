
"""
from setuptools import setup
import setuptools

setup(
    name='PokerInPython',
    version='1.0.0',
    packages=setuptools.find_packages(),
    package_dir={'': 'PokerInPython'},
    url='https://github.com/Smith1999Tom/PokerInPython',
    license='',
    author='Tom Smith',
    author_email='smith1999tom@gmail.com',
    description='A poker game made with pygame',
    keywords='poker python pygame'
)
"""

import cx_Freeze
executables = [cx_Freeze.Executable("PokerInPython.py")]

cx_Freeze.setup(

    name="Poker in Python",

    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["./Images", "./Sounds", "./Font"]
                           }},

    executables=executables

    )