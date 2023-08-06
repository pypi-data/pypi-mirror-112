from setuptools import setup, find_packages

setup(
    name='PyMPDATA-examples',
    version='0.2',
    setup_requires=['setuptools_scm'],
    install_requires=['PyMPDATA',
                      'pystrict',
                      'matplotlib',
                      'ipywidgets',
                      'scipy',
                      'pint',
                      'joblib',
                      'sympy',
                      'ghapi'],
    author='https://github.com/orgs/atmos-cloud-sim-uj/people',
    license="GPL-3.0",
    packages=find_packages(include=['PyMPDATA_examples', 'PyMPDATA_examples.*']),
    package_data={'': ['*/*/*.txt']},
    include_package_data=True
)
