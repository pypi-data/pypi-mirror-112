from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Auto1 ETL Challenge'

# Setting up
setup(
    name="etlpkg",
    version=VERSION,
    author="Muhammad Aqib",
    author_email="<inbox.aqib@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['auto1','etl'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)