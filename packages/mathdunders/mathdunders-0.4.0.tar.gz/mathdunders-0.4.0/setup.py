from os import path
from setuptools import setup

version = "0.4.0"

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='mathdunders',
    version=version,
    author='discretegames',
    author_email='discretizedgames@gmail.com',
    description="Decorator that automatically adds math dunders to a class.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/discretegames/mathdunders',
    packages=['mathdunders'],
    license="MIT",
    keywords=['python', 'math', 'mathematics', 'dunder', 'double under', 'underscore', 'magic method', 'number']
)
