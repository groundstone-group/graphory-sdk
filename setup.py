from setuptools import setup, find_packages

setup(
    name="graphory",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["httpx>=0.24"],
    author="Graphory",
    author_email="hello@graphory.io",
    description="Python SDK for the Graphory Knowledge Graph API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/groundstone-group/graphory-sdk",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
