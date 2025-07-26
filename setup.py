from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enable-ai-sdk",
    version="1.0.0",
    author="EnableAI Team",
    author_email="support@enable.ai",
    description="A comprehensive Python SDK for the EnableAI Agentic AI Platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://www.weenable.ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="ai, agent, analytics, feedback, webhooks, self-healing",
    project_urls={
        "Bug Reports": "https://github.com/dmartin4506/enable-ai-sdk/issues",
        "Source": "https://github.com/dmartin4506/enable-ai-sdk",
        "Documentation": "https://www.weenable.ai",
    },
) 