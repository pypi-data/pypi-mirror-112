import os
import setuptools

here = os.path.join(os.path.dirname(__file__))

__version__ = None
with open(os.path.join(here, 'flagsense', 'version.py')) as _file:
	exec(_file.read())

with open(os.path.join(here, 'requirements', 'core.txt')) as _file:
	REQUIREMENTS = _file.read().splitlines()

with open(os.path.join(here, 'README.md')) as _file:
	README = _file.read()

setuptools.setup(
	name='flagsense-sdk',
	version=__version__,
	author="Flagsense",
	author_email='senseflag@gmail.com',
	description='Flagsense sdk for python',
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/flagsense/flagsense-python-sdk',
	packages=setuptools.find_packages(exclude=['test']),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
	],
	install_requires=REQUIREMENTS,
)
