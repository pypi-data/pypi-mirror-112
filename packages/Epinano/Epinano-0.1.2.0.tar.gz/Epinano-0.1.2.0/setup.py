from setuptools import setup

with open ('README','r') as fh:
    long_description = fh.read()

with open ('requirements.txt', 'r') as fh:
    required = fh.read().splitlines()

setup (
    name='Epinano',
    url='https://github.com/enovoa/EpiNano',
    version='0.1.2.0',
    description='call variants, compute variants frequencies from bam file and use the frequencies to predict RNA base modifications',
    py_modules=[],
    package_dir={'':'src'}, 
    author='Huanle Liu && Eva Novoa',
    author_email='huanle.liu@crg.eu',
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=required
)
