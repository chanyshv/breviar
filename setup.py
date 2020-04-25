from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="breviar",
    version="0.0.1c",
    packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'colorama>=0.4.3',
        'click>=7.1.1',
        'cerberus>=1.3.2',
        'requests>=2.0'
    ],
    entry_points={
        'console_scripts': [
            'breviar = breviar.entrypoint:entrypoint'
        ]},
    author='Damir Chanyshev',
    author_email='hairygeek@yandex.com',
    description='URL shortener cli',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='link url shortener cli bilty',
    project_urls={
        "Bug Tracker": "https://github.com/hairygeek/breviar",
        "Documentation": "https://github.com/hairygeek/breviar",
        "Source Code": "https://github.com/hairygeek/breviar",
    }
)
