import os
import shutil

from setuptools import setup, find_packages

package_name = "nztm"
package_version = '0.0.3'

egg_info = "%s.egg-info" % package_name
if os.path.isdir(egg_info):
    shutil.rmtree(egg_info)

requirements = []

setup(
    name="nztm",
    packages=find_packages(exclude=["test"]),
    # package_data={'vortex': ['*.xml']},
    version=package_version,
    install_requires=requirements,
    description="Geo coordinate conversion library between NZTM2000 and WGS84",
    author="Synerty",
    author_email="contact@synerty.com",
    url="https://github.com/Synerty/nztm",
    download_url=(
            "https://github.com/Synerty/%s/tarball/%s" % (package_name, package_version)
    ),
    keywords=["nztm", "geo", "coordinate", "synerty"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
)
