from setuptools import setup

with open('README.md', 'r') as file:
    README = file.read()
    file.close()

setup(
    name="OnlineWorks",
    version="0.0.5",
    description="A simple python pacakage that helps you to perform sevaral online tasks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/OnlineWorks",
    author="Debadrito Dutta",
    author_email="dipalidutta312@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["OnlineTasks"],
    include_package_data=False,
    install_requires=['requests', 'bs4', 'opencv-python', 'numpy', 'wikipedia', 'pyautogui'],
    entry_points={
        "console_scripts": [
            "OnlineTasks=OnlineTasks.__init__:main",
        ]
    }
)
