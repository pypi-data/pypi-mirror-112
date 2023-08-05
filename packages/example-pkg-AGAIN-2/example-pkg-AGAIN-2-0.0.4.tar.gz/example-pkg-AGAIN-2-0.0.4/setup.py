#setup.py
from setuptools import setup, find_packages
import setuptools

MAIN_REQUIREMENTS = [
    "streamlit==0.83.0",
    "google-cloud==0.34.0",
    "google-cloud-bigquery==2.20.0",
]

TEST_REQUIREMENTS = [
    "pytest>=3.7"
]

CLASSIFIERS = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="example-pkg-AGAIN-2",
    version="0.0.4",
    author="Beepbeep Technology",
    author_email="contact@beepbeep.technology",
    description="Sync data transformation information from BigQuery to GitHub and create a dynamic Markdown documantation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beepbeeptechnology/sync_from_bigquery_to_github",
    project_urls={
        "Bug Tracker": "https://github.com/beepbeeptechnology/sync_from_bigquery_to_github/issues",
    },
    classifiers=CLASSIFIERS,
    package_dir={"": "bases"},
    packages=setuptools.find_packages(where="bases"),
    install_requires=MAIN_REQUIREMENTS,
    extra_require={
        "dev": TEST_REQUIREMENTS
    },
    python_requires=">=3.6",
)
