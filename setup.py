from setuptools import setup, find_namespace_packages
import subprocess


def determine_version():
    # Examples (git describe -> python package version):
    # 4.1.1-0-gad012482d -> 4.1.1
    # 4.1.1-16-g2d8943dbc -> 4.1.1.post16+g2d8943dbc
    #
    # For shallow clones or repositories missing tags:
    # 0ae7c04
    desc = (
        subprocess.run(
            ["git", "describe", "--tags", "--long"],
            stdout=subprocess.PIPE,
            check=False,
            text=True,
        )
        .stdout
        .strip()
    )

    split_desc = desc.split("-")
    assert (
            len(split_desc) == 3
    ), f"Failed to parse lens-flow git version description {desc!r}."

    version = split_desc[0]
    distance = split_desc[1]
    commit = split_desc[2]

    if distance == "0":
        return version

    return f"{version}.post{distance}+git{commit[1:]}"


# Common distribution data
name = "lens-flow"
description = "An applet to stream pi camera over http."
author_email = "online@wolog.org"
python_version = "3.10.*"
url = "https://github.com/FC-Rover/LensFlow.git"
license_ = "GPL v3"
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
]

install_requires = [
    "picamera2",
]

setup(
    name=name,
    python_requires=f"=={python_version}",
    version=determine_version(),
    description=description,
    author_email=author_email,
    url=url,
    packages=find_namespace_packages(),
    license=license_,
    classifiers=classifiers,
    entry_points=dict(
        console_scripts=[
            "lens-flow = server:main",
        ]
    ),
    install_requires=install_requires,
)
