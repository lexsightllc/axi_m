# SPDX-License-Identifier: MIT
from setuptools import setup, find_packages

setup(
    name='axiomm',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'pytest',
    ],
    author='Augusto Ochoa Ughini (Conceptual Author)',
    description='Architectural eXpansive Interface for Ontological Mediation (AXIΩM) - a prototype.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ochoaughini/.1',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.9',
)
