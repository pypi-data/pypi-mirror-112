# -*- coding: utf-8 -*-
import os
import platform
import sys
import subprocess
from os import path
import shutil
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            "-DEXAMPLE_VERSION_INFO={}".format(
                self.distribution.get_version()),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),
            "-DCMAKE_POSITION_INDEPENDENT_CODE=on"

        ]
        build_args = []

        if platform.system() == "Darwin":
            cmake_args += ["-DOPENSSL_ROOT_DIR=/usr/local/opt/openssl",
                           "-DOPENSSL_LIBRARIES=/usr/local/opt/openssl/lib"]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator:
                cmake_args += ["-GNinja"]

        else:

            # Single config generators are handled "normally"
            single_config = any(
                x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Multi-config generators have a different way to specify configs
            if not single_config:
                build_args += ["--config", cfg]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )

        wrapper_path = path.join(self.build_temp, 'src/python_wrapper')
        if not os.path.exists(extdir):
            os.mkdir(extdir)
        print(f"Wrapper path: {wrapper_path}")
        for file in os.listdir(wrapper_path):
            if file.endswith(".so"):
                file_path = path.join(wrapper_path, file)

                shutil.copy(file_path, extdir)


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="secyan_python",
    author="Qiwei Li",
    author_email="sirily1997@gmail.com",
    description="SECYAN c++ implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension("secyan_python")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    platforms=['any'],
    classifiers=['Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9', ],
    python_requires='>=3.6',
    packages=find_packages(),
    setup_requires=['setuptools-git-versioning'],
    version_config={
        "template": "{tag}",
    },
)
