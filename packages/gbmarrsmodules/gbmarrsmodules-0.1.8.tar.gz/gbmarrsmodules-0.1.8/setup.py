import setuptools
from setuptools import setup, find_packages
import os
# Set the proposed version number before committing
setup(name='gbmarrsmodules',
    version=f'0.1.8',
    description='Shared common modules from General Bioinformatics',
    url='https://gitlab.generalbioinformatics.com/dev-all/gbmarrsmodules',
    author='Mike Way, Joanna Parmley, Eleanor Cottam',
    author_email='mike.way@generalbioinformatics.com, joanna@generalbioinformatics.com',
    license='MIT',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'rdflib',
        'pandas',
        'requests',
        'psycopg2-binary',
        'jinja2',
        'jprops'
    ],
    zip_safe=False)
      
