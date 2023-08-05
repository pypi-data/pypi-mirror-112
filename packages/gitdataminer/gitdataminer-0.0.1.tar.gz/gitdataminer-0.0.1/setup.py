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


VERSION = "0.0.1"  # MAJOR.MINOR.MICRO
DESCRIPTION = "Git logs analyzer"
LONG_DESCRIPTION = "Git logs analyzer which analyzes the metrics regarding total commits,\
    commits per year, commits per month, top 10 author, total commits by author, \
    coding days, churn, author insertion rate, productive day and so on"

CLASSIFIERS = """\
Development Status :: 3 - Alpha
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


setup(
    name="gitdataminer",
    version=VERSION,
    author="Tushant Khatiwada && Manish Yadav",
    author_email="programmertushant@gmail.com,manish.sinuwari@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="src"),
    # install_requires=open("requirements.text").read(),
    keywords=["python", "git analyzer", "git data science"],
    py_modules=["gitdataminer"],
    classifiers=[classifier for classifier in CLASSIFIERS.split("\n") if classifier],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    test_suite="pytest",
    python_requires=">=3.7",
    package_dir={"": "src"},
    install_requires=[
        'matplotlib==3.4.2',
        'pandas==1.2.5',
        'numpy==1.21.0'
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },

)
