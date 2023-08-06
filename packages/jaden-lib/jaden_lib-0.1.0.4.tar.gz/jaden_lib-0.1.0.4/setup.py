import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jaden_lib",
    version="0.1.0.4",
    author="Jaden Lee",
    author_email="zhuoen.li@outlook.com",
    description="A library of Jaden.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/liling",
    project_urls={
        "Bug Tracker": "https://gitee.com/liling",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)
