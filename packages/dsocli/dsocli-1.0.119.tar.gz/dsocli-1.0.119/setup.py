#!/usr/bin/self.env python
import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command
from distutils.version import StrictVersion
import requests
import json

# Package meta-data.
NAME = 'dsocli'
DESCRIPTION = 'DSO CLI'
REQUIRES_PYTHON = '>=3.0'
URL = "https://github.com/ramtinkazemi/dsocli"
EMAIL = 'ramtin.kazemi@gmail.com'
AUTHOR = 'Ramtin Kazemi'
MAJOR_VERSION = 1
MINOR_VERSION = 0
PATCH_VERSION = -1  ### for automatic patch versioning set to -1

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

# ------------------------------------------------------------------------

### set_long_description
try:
    with io.open(os.path.join(here, 'PyPI-Description.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

### set_pypi_index
git_branch = os.popen('git symbolic-ref --short HEAD').read().strip()
if git_branch == 'master':
    env='prod'
    pypi_index='pypi'
    pypi_url='https://pypi.org/pypi/dsocli/json'
elif git_branch == 'develop':
    env='dev'
    pypi_index='testpypi'
    pypi_url='https://test.pypi.org/pypi/dsocli/json'
else:
    raise Exception("Only 'develop' and 'master' git_branches can be deployed.")

### set version
published_versions = list(reversed(sorted(requests.get(pypi_url).json()['releases'].keys(), key=StrictVersion)))

if not published_versions: 
    current_version = f"{MAJOR_VERSION}.{MINOR_VERSION}.0"
else:
    current_version = published_versions[0]

current_major = int(current_version.split('.')[0])
current_minor = int(current_version.split('.')[1])
current_patch = int(current_version.split('.')[2])
new_major = MAJOR_VERSION
new_minor = MINOR_VERSION
if new_major < current_major:
    raise Exception(f"New version '{new_major}.x.x' must be greater than the current version '{current_major}.x.x'.")
elif new_major == current_major:
    if new_minor < current_minor:
        raise Exception(f"New version '{new_major}.{new_minor}.x' must be greater than the current version '{current_major}.{current_minor}.x'.")
    elif new_minor == current_minor:
        new_patch = current_patch + 1 if PATCH_VERSION == -1 else PATCH_VERSION
        if new_patch <= current_patch:
            raise Exception(f"New version '{new_major}.{new_minor}.{new_patch}' must be greater than the current version '{current_major}.{current_minor}.{current_patch}'.")
    ### minor version increased
    else:
        new_patch = 1 if PATCH_VERSION == -1 else PATCH_VERSION
### major version increased
else:
    new_patch = 1 if PATCH_VERSION == -1 else PATCH_VERSION


new_version = f"{new_major}.{new_minor}.{new_patch}"
if not env == 'prod':
    new_version += f".{env}"

with open(os.path.join(here, 'src', NAME, 'package.json'), 'r') as f:
    package_info = json.load(f)
package_info['version'] = new_version
with open(os.path.join(here, 'src', NAME, 'package.json'), 'w') as f:
    json.dump(package_info, f, sort_keys=False, indent=2)

# ------------------------------------------------------------------------

class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
        
    def run(self):
        
        self.status(f"Git Branch={git_branch}\nEnv={env}\nPyPI Index={pypi_index}\nCurrent Version={current_version}\nNew Version={new_version}")
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'build'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        ### read from ~/.pypirc
        # TWINE_PASSWORD=$(<pypi-token.secret) python -m twine upload --username __token__ --skip-existing --repository testpypi dist/*
        code = os.system('{0} -m twine upload --skip-existing --repository {1} dist/*'.format(sys.executable, pypi_index))

        sys.exit(code)

        

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

setup(
    name=NAME,
    version=new_version,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    project_urls={
        'Documentation': URL,
        'Source': URL
    },
    packages=find_packages('src', exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir = { '' : 'src/' }, 
    setup_requires=['wheel'],
    python_requires=REQUIRES_PYTHON,
    install_requires=open(os.path.join(here, 'requirements/prod.in'), 'r').readlines(),
    extras_require=None,
    package_data={'': ['package.json']},
    include_package_data=True,
    license='GPLV3',
    license_files = ['LICENSE.md'],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    entry_points={
        # 'distutils.commands': ['publish = package.module:publish_command'],
        'console_scripts': [f'dso = {NAME}.cli:cli'],
        },
    cmdclass={'publish': PublishCommand},
)
