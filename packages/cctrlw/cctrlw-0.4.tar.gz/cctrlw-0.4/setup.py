import os

import cctrlw
from setuptools import find_packages, setup


def install(appname):

    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as fobj:
        readme = fobj.read()

    setup(
        name=appname,
        version=cctrlw.VERSION,
        description="""Configurable Ctrl-W algorithm, xontrib and CLI.""",
        long_description=readme,
        long_description_content_type="text/x-rst",
        url="https://github.com/ggdwbg/cctrlw",
        download_url="https://pypi.python.org/cctrlw/",
        license="MIT",
        platforms="any",
        classifiers=[  # copypasted from github of some package
            "Intended Audience :: End Users/Desktop",
            "License :: Freeware",
            "Programming Language :: Python",
        ],
        py_modules=["cctrlw", "cctrlw.cli", "cctrlw.algo"],
        packages=["xontrib", cctrlw.CONFIG_DIR],
        package_dir={"xontrib": "xontrib"},
        package_data={
            cctrlw.CONFIG_DIR: [cctrlw.MODES_JSON],
            "xontrib": ["*.xsh", "*.py"],
        },
        install_requires=["cctrlw"],
        author="Maxim Yurchenkov",
        author_email="ggdwbg@gmail.com",
        include_package_data=True,
    )


if __name__ == "__main__":
    import sys

    install("cctrlw")
