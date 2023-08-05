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

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bqtxflowutils-2",
    version="0.0.5",
    author="Beepbeep Technology",
    author_email="contact@beepbeep.technology",
    description="Sync data transformation information from BigQuery to GitHub and create a dynamic Markdown documantation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beepbeeptechnology/sync_from_bigquery_to_github",
    package_dir={
            "beepbeep_txflowutils": "beepbeep_txflowutils",
            "beepbeep_txflowutils.auth": "beepbeep_txflowutils/auth",
            "beepbeep_txflowutils.github_source": "beepbeep_txflowutils/github_source",
            "beepbeep_txflowutils.secrets": "beepbeep_txflowutils/secrets",
            "beepbeep_txflowutils.secrets.service_account_credentials": "beepbeep_txflowutils/secrets/service_account_credentials",
            "beepbeep_txflowutils.utils": "beepbeep_txflowutils/utils",
        },
    packages=[
            "beepbeep_txflowutils", 
            "beepbeep_txflowutils.auth", 
            "beepbeep_txflowutils.github_source",
            "beepbeep_txflowutils.secrets",
            "beepbeep_txflowutils.secrets.service_account_credentials",
            "beepbeep_txflowutils.utils"
        ],
    classifiers=CLASSIFIERS,
    install_requires=MAIN_REQUIREMENTS,
    extra_require={
        "dev": TEST_REQUIREMENTS
    },
    python_requires=">=3.6",
)