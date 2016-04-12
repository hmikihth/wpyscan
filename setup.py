import os
from setuptools import setup

datadir = 'usr'
datafiles = []

for d, folders, files in os.walk(datadir):
    datafiles.append((os.path.join('/',d), [os.path.join(d, file) for file in files]))
    
print (datafiles)

setup(
    name="wpyscan",

    version="0.1",

    description="Wordpress pentest tool",
    long_description="Search exploits on exploit-db, wordpressexploit.com and wpvulndb.com according to recon informations (version, modules and theme).",

    url="https://github.com/Ganapati/wpyscan",

    author="ganapati (@G4N4P4T1)",

    license="BEER-WARE",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: System Administrators",

        "Topic :: Utilities",

        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: BSD :: OpenBSD",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],

    packages=["wpyscan"],
    
    scripts=["bin/wpyscan"],
    
    data_files=datafiles,
)
