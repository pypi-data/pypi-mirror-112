import setuptools
from setuptools import find_packages

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Alec Lumsden",
    author_email="aleclumsden@berkeley.edu",
    name='lranalyzer',
    license="MIT",
    description='Learning rate tuning for keras models',
    version='v0.0.4.0.4',
    long_description=README,
    url='',
    packages= find_packages(
        where = 'src',
        include = ['lranalyzer*',],
    ),
    package_dir = {"":"src"},
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)