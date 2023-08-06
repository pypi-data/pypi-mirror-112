import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rgb",  # Replace with your own username
    version="0.0.2",
    author="Seungjae Ryan Lee",
    author_email="seungjaeryanlee@gmail.com",
    description="Grab your palette!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seungjaeryanlee/rgb",
    project_urls={
        "Bug Tracker": "https://github.com/seungjaeryanlee/rgb/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
