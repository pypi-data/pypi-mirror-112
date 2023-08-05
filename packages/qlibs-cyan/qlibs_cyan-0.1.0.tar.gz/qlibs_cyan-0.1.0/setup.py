import setuptools
from setuptools import Extension
import traceback

with open("README.md", "r") as fh:
    long_description = fh.read()

def do_setup(ext_modules):
    setuptools.setup(
        name="qlibs_cyan",
        version="0.1.0",
        author="IQuant",
        author_email="quant3234@gmail.com",
        description="C modules for qlibs",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/IntQuant/qlibs-cyan/",
        packages=setuptools.find_packages(),
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        install_requires=[],
        extras_require={
        },
        ext_modules=ext_modules,
        zip_safe=False,
    )

do_setup([Extension("qlibs_cyan.math.mat4", ["qlibs_cyan/math/mat4.c"])])
