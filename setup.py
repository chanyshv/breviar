from setuptools import setup, find_namespace_packages

setup(
    name="slink",
    version="0.0.1",
    packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'colorama>=0.4.3',
        'click>=7.1.1',
        'cerberus>=1.3.2',
    ],
    entry_points={
        'console_scripts': [
            'slink = slink.entrypoint:entrypoint'
        ]}
)
