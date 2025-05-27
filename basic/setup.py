from setuptools import setup, find_packages

setup(
    name="dialogchain-basic-examples",
    version="0.1.0",
    description="Basic examples for DialogChain",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
)
