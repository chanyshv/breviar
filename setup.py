from setuptools import setup, find_namespace_packages

setup(
    name="slink",
    version="0.0.1b",
    packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'colorama>=0.4.3',
        'click>=7.1.1',
        'cerberus>=1.3.2',
        'requests>=2.0'
    ],
    entry_points={
        'console_scripts': [
            'slink = slink.entrypoint:entrypoint'
        ]},
    author='Damir Chanyshev',
    author_email='hairygeek@yandex.com',
    description='URL shortener cli',
    keywords='link url shortener cli bilty',
    project_urls={
        "Bug Tracker": "https://github.com/hairygeek/slink",
        "Documentation": "https://github.com/hairygeek/slink",
        "Source Code": "https://github.com/hairygeek/slink",
    }
)
