import sys
import os

if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version >= 3.7 required.")

# BEFORE importing setuptools, remove MANIFEST. Otherwise it may not be
# properly updated when the contents of directories change (true for distutils,
# not sure about setuptools).
if os.path.exists("MANIFEST"):
    os.remove("MANIFEST")


from setuptools import setup, find_packages


VERSION = "0.0.3"  # MAJOR.MINOR.MICRO
DESCRIPTION = "Git logs analyzer"
LONG_DESCRIPTION = "Git logs analyzer which analyzes the metrics regarding total commits,\
    commits per year, commits per month, top 10 author, total commits by author, \
    coding days, churn, author insertion rate, productive day and so on"

CLASSIFIERS = """\
Development Status :: 1 - Planning
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3 :: Only
Topic :: Software Development
"""


# setup
setup(
    name="gitdataminer",
    version=VERSION,
    author="Tushant Khatiwada && Manish Yadav",
    author_email="programmertushant@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="./src", exclude=("./backup",)),
    include_package_data=True,
    py_modules=["gitdataminer"],
    package_dir={"": "src"},
    install_requires=["matplotlib==3.4.2", "pandas==1.2.5", "numpy==1.21.0"],
    keywords=["python", "git analyzer", "git data science"],
    classifiers=[classifier for classifier in CLASSIFIERS.split("\n") if classifier],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    test_suite="pytest",
    python_requires=">=3.7",
)
