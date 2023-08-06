from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Local file updater'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name='file-updater',
    version=VERSION,
    author='Daniel Riffert',
    author_email='riffert.daniel@gmail.com',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    py_modules=['updater', 'progress_bar'],
    package_dir={'':'fup'},
    #packages=find_packages(),
    scripts=['fup/fup.py'],
    install_requires=['colorama', 'pywin32'],
    keywords=['file', 'update', 'path', 'backup'],
    # classifiers=[
    #     "Development Status :: 1 - Planning",
    #     "Intended Audience :: Developers",
    #     "Programming Language :: Python :: 3",
    #     "Operating System :: Unix",
    #     "Operating System :: MacOS :: MacOS X",
    #     "Operating System :: Microsoft :: Windows",
    # ]
)