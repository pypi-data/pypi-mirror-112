import codecs
import os.path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split('"')[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="tpi-connector",
    version=get_version(os.path.join("tpi_connector", "__init__.py")),
    author="Soral",
    author_email="admin@top-infra.com",
    description="Restful connector to tpi-compliance applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/top-infra/tpi-connector",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
