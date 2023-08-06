from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='testing101',
    version='0.0.1',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ashutoshaks/testing101',
    author='Ashutosh Kumar Singh',
    author_email='asingh@blotout.io',
    packages=find_packages(),  # Required
    python_requires='>=3.7, <4',
)
