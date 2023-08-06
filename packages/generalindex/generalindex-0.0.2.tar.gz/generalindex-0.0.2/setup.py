import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generalindex",
    version="0.0.2",
    author="General Index",
    author_email="info@genral-index.com",
    description="Python SDK for the General Index platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.general-index.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
