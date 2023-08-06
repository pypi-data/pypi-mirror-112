# coding: utf-8
import setuptools

VERSION = "0.0.8b0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="niiif-niiif",                     # This is the name of the package
    version=VERSION,                        # The initial release version
    author="Jean-Baptiste Pressac",        # Full name of the author
    url="https://gitlab.huma-num.fr/jpressac/niiif-niiif",
    project_urls={
        "Issues": "https://gitlab.huma-num.fr/jpressac/niiif-niiif/-/issues",
        "CI": "https://gitlab.huma-num.fr/jpressac/niiif-niiif/-/pipelines",
        "Changelog": "https://gitlab.huma-num.fr/jpressac/niiif-niiif/-/blob/master/CHANGELOG.md",
    },
    description="Création et dépôt de manifestes IIIF pour des données déposées sur Nakala",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["niiif"],                   # Name of the python package
    package_dir={'':'niiif-niiif/src'},     # Directory of the source code of the package
    install_requires=['requests']           # Install other dependencies if any
)