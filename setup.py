import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AlteryxGalleryAPI",
    version="0.0.7",
    author="PAUL HOUGHTON",
    author_email="paul.houghton@theinformationlab.co.uk",
    description="An API for connecting to an Alteryx Gallery. Forked from the project by DAVID PRYOR, NICK SIMMONS, AND RITU GOWLIKAR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sivivatu/AlteryxGalleryAPI",
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',  
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ),
    package_dir={'': 'src'},
    packages = setuptools.find_packages(where='src'),
    install_requires = ['pandas', 
        'requests'],
    dependency_links=[
        'https://pypi.org/project/pandas/'
    ],
    project_urls={
        'API Documentation': 'https://gallery.alteryx.com/api-docs/',
        'Source': 'https://github.com/Sivivatu/AlteryxGalleryAPI',
        'Bug Tracker': 'https://github.com/Sivivatu/AlteryxGalleryAPI/issues',
    }
)