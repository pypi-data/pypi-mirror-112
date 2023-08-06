from glob import glob
import os
import sys
from glob import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

windows = sys.platform.startswith("win")

include_dirs = [
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'common')),
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'wikipedia')),
]
lib_dirs = []
libs = ['pcre']
comp = []
macros = [('PCRE_STATIC', None)]

if windows:
    PCRE_HOME = os.environ.get("PCRE_HOME", os.path.realpath(os.path.join(__file__, '..', 'pcre')))
    print('PCRE_HOME', PCRE_HOME)
    include_dirs.append(PCRE_HOME)
    lib_dirs.append(PCRE_HOME)
    macros.append(('CLOCK_MONOTONIC', None))
    macros.append(('clock_gettime', '//'))
else:
    comp.append('-std=c++11')

setuptools.setup(
    name="pyautocorpus",
    version="0.1.0",
    author="Sean MacAvaney",
    author_email="sean.macavaney@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanmacavaney/pyautocorpus",
    include_package_data = True,
    packages=setuptools.find_packages(include=['pyautocorpus']),
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    ext_modules=[setuptools.Extension("pyautocorpus", [
        "src/pyautocorpus.cpp",
        "AutoCorpus/src/common/utilities.cpp",
        "AutoCorpus/src/wikipedia/Textifier.cpp",
    ], include_dirs=include_dirs, libraries=libs, define_macros=macros, extra_compile_args=comp)],
)
