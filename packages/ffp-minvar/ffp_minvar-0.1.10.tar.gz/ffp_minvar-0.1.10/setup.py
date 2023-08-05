import setuptools
from setuptools.command.install import install

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
from platform import system
import sys
import os
import shutil as sh


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# define some flags and dirs
gcc_args = []
gcc_build_flags = []
lib_name = ''

# Check if windoes linnux or mac to pass flag
if system() == 'Windows':
    if sys.maxsize // 2 ** 32 > 0:
        gcc_args[-1] += ' Win64'
    gcc_build_flags += ['--config', 'Release']
    lib_name = 'alg_lomv.dll'
else: # Linux or Mac
    gcc_args += ['-shared', '-o']
    gcc_build_flags += ['-lm', '-lgsl', '-lgslcblas', '-g']
    lib_name = 'alg_lomv.so'


# Define src, header and bulid directories
current_dir = os.getcwd()
alglomv_src_dir = os.path.join(current_dir, 'src')
src_file = os.path.join(alglomv_src_dir, 'alg_lomv.c')
alglomv_h_dir = os.path.join(current_dir, 'include')
header_file = os.path.join(alglomv_h_dir, 'alg_lomv.h')

build_dir = os.path.join(current_dir, 'build')
shard_lib = os.path.join(build_dir, lib_name)

"""
class build_ext_alglomv(build_ext):
    def run(self):
        # Create build directory
        if os.path.exists(build_dir):
            sh.rmtree(build_dir)
        os.makedirs(build_dir)
        os.chdir(build_dir)

        # bulid shared library
        call(['gcc'] + gcc_args + [lib_name] + [src_file] + gcc_build_flags)

        # Change directory back to the python interface
        os.chdir(current_dir)

        build_ext.run(self)


_alg_lomv = Extension(lib_name,
                    sources = ['src/alg_lomv.c'],
                    include_dirs= ['include']
                    )


# setuptools.setup
setup(
    name="ffp_minvar",
    version="0.1.9",
    author="Lucius Luo",
    author_email="lucius0228@gmail.com",
    description="rewritten python package of ffp_minvar algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luciusluo/ffp_minvar",
    project_urls={
        "Bug Tracker": "https://github.com/luciusluo/ffp_minvar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),
    python_requires=">=3.6",
    include_package_data=True, # might delete later
    # ext_modules = [_alg_lomv]
    cmdclass={'build_ext': build_ext_alglomv}
)
"""

class CustomInstall(install):
    def run(self):
        command = "git clone https://github.com/luciusluo/ffp_minvar.git"
        process = subprocess.Popen(command, shell=True, cwd="lib")
        process.wait()
        install.run(self)

_alg_lomv = Extension(lib_name,
                    sources = ['src/alg_lomv.c'],
                    include_dirs= ['include'],
                    extra_link_args=gcc_build_flags
                    )


setup(
    name="ffp_minvar",
    version="0.1.10",
    author="Lucius Luo",
    author_email="lucius0228@gmail.com",
    description="rewritten python package of ffp_minvar algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luciusluo/ffp_minvar",
    project_urls={
        "Bug Tracker": "https://github.com/luciusluo/ffp_minvar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "lib"},
    packages=setuptools.find_packages(where="lib"),
    python_requires=">=3.6",
    include_package_data=True, # might delete later
    ext_modules = [_alg_lomv],
    cmdclass={'install': CustomInstall}
    
)