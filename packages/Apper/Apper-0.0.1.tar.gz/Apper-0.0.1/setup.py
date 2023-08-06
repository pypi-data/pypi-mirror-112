import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Apper",
    version="0.0.1",
    author="parsa_Mehrabi",
    author_email="mamy4853@gmail.com",
    description="this is for Create Application Window",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "Apper"},
    packages=setuptools.find_packages(where="Apper"),
    python_requires=">=3.8",
    
)