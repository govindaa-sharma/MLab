from setuptools import setup, find_packages

setup(
    name="experiment_ai",
    version="0.1.0",
    description="SDK for logging ML experiments",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
)