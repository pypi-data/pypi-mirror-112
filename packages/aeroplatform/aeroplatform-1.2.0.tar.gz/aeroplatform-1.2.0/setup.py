import setuptools
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSIONFILE="aeroplatform/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name="aeroplatform",
    version=verstr,
    author="Aero Technologies",
    author_email="aero@robbiea.co.uk",
    description="A simple Data Infrastructure Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'click>=7.0',
        'requests',
        'boto3',
        'pylint<2.5.0',
        'aero-metaflow'
    ],
    entry_points={
        'console_scripts': [
            'aero = aeroplatform.cli:cli',
        ],
    },
    include_package_data=True,
    package_data={
        "aeroplatform": [
            "config.json"
        ]
    }
)