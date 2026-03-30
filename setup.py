"""setup.py for spectral_sandbox."""
from setuptools import setup, find_packages

with open("docs/README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spectral-sandbox",
    version="0.1.0",
    author="BrewtaniusAI",
    description="Spectral methods toolkit: ISEP checks, operator construction, and proof vault.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BrewtaniusAI/Sprectral-Sandbox",
    packages=find_packages(exclude=["tests*", "examples*"]),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "jupyter>=1.0",
            "matplotlib>=3.5",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    license="MIT",
)
