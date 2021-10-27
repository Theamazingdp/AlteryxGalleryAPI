import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AlteryxGalleryAPI",
    version="0.1.1",
    author="PAUL HOUGHTON",
    author_email="paul.houghton@theinformationlab.co.uk",
    description="An API for connecting to an Alteryx Gallery. Forked from the project by DAVID PRYOR, NICK SIMMONS, AND RITU GOWLIKAR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sivivatu/AlteryxGalleryAPI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
    ),
    project_urls={
        'API Documentation': 'https://gallery.alteryx.com/api-docs/',
        'Source': 'https://github.com/Sivivatu/AlteryxGalleryAPI',
        'Bug Tracker': 'https://github.com/Sivivatu/AlteryxGalleryAPI/issues',
    },
    install_requires = ['pandas', 
        'requests']
)