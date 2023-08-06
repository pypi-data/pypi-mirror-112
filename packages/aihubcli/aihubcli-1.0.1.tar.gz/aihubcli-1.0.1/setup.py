from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf8")

# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and ( not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs  if 'git+' not in x]

setup (
 name = 'aihubcli',
 description = 'A simple cli utility to generate ML project structure for quickly starting ML projects',
 version = '1.0.1',
 packages = find_packages(), # list of all packages
 package_data={ 'aihubcli': ['templates/*.zip'] },
 install_requires = install_requires,
 python_requires='>=2.7', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        aihubcli = aihubcli.__main__:cli
    ''',
 author="Vikram Soni",
 keyword="ML, project, aihub, structure, skeleton, generator, cli",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
#  url='https://github.com/vikramsoni2/aihub-cli',
#  download_url='https://github.com/CITGuru/cver/archive/1.0.0.tar.gz',
 dependency_links=dependency_links,
 author_email='vikram9880@gmail.com',
 classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)