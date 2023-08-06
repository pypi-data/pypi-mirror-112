from setuptools import setup, find_packages
import pathlib
import subprocess
import os

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

testing101_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in testing101_version
with open("mypackage/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{testing101_version}\n")

setup(
    name='testing101',
    version=testing101_version,
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ashutoshaks/testing101',
    author='Ashutosh Kumar Singh',
    author_email='asingh@blotout.io',
    packages=find_packages(),  # Required
    python_requires='>=3.7, <4',
    package_data={
        'mypackage': ['VERSION'],
    },
)
