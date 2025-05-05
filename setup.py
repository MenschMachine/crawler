from setuptools import setup, find_packages

setup(
    name="usual-suspects-crawler",  # Consider a more unique name like "web-md-crawler" to avoid conflicts on PyPI
    version="0.1.0",  # This will be managed by your release process
    author="Michael Lahr",
    author_email="michael.lahr@gmail.com",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "html2text",
        "matplotlib",  # For visualization
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "crawler=crawler:main",
        ],
    },
    description="A simple web crawler that converts HTML content to Markdown",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MenschMachine/crawler",  # Add your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
