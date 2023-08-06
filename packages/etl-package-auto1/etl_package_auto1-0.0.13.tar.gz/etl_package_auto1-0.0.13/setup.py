from setuptools import setup, find_packages

VERSION = '0.0.13'
DESCRIPTION = 'ETL Package Auto1'

# Setting up
setup(
    name="etl_package_auto1",
    version=VERSION,
    author="Muhammad Aqib",
    author_email="<inbox.aqib@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['etl','auto1'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)