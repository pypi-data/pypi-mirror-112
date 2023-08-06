# Original Author    : Edwin G. W. Peters @ sdr-Surface-Book-2
#   Creation date    : Fri Jun 25 10:35:09 2021 (+1000)
#   Email            : edwin.peters@unsw.edu.au
# ------------------------------------------------------------------------------
# Last-Updated       : Fri Jun 25 11:07:37 2021 (+1000)
#           By       : Edwin G. W. Peters @ sdr-Surface-Book-2
# ------------------------------------------------------------------------------
# File Name          : setup.py
# Description        : 
# ------------------------------------------------------------------------------
# Copyright          : Insert license
# ------------------------------------------------------------------------------


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='pyLoadModularJson',
    version='0.9.0',
    packages=setuptools.find_packages(),
    url='https://github.com/mugpahug/pyLoadModularJson',
    license='MIT',
    author='Edwin Peters',
    author_email='edwin.g.w.peters@gmail.com',
    description='Load nested JSON files into a dictionary',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='json,config,modular,nested',
    install_requires=[
        'rjsmin'],
)

