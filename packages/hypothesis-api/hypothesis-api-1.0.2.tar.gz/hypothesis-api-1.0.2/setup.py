import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypothesis-api",
    version="1.0.2",
    author="Jon Udell",
    author_email="judell@hypothes.is",
    description="Python wrapper for the Hypothesis annotation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/judell/hypothesis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)