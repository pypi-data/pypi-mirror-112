import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OnlineWorks",
    version="0.0.1",
    author="Debadrito Dutta",
    author_email="dipalidutta312@gmail.com",
    description="A python package that helps you to perform sevaral online tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/OnlineWorks",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/OnlineWorks/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.4",
)
