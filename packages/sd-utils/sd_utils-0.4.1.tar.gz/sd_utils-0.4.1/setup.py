from setuptools import setup, find_packages


with open("README.md", "r") as file:
    readme = file.read()


with open("requirements.txt", "r") as fp:
    requires = fp.read().splitlines()

setup(
    name="sd_utils",
    version="0.4.1",
    description="A python module with basic utils I tend to use in my projects",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(),
    url="https://github.com/stephend017/sd_utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
)
