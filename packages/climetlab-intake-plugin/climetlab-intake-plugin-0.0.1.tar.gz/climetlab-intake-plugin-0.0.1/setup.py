import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


version = "0.0.1"


setuptools.setup(
    name="climetlab-intake-plugin",
    version=version,
    description="Climetlab Intake source plugin",
    long_description=read("README.md"),
    author="Ashwin Samudre",
    author_email="capnoi8@gmail.com",
    license="Apache License Version 2.0",
    url="https://github.com/esowc/climetlab-intake-plugin",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=["intake", "intake-xarray", "intake-iris", "intake-sklearn", "pandas"],
    zip_safe=True,
    entry_points={
        "climetlab.sources": ["intake = climetlab_intake:Intake"]
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)