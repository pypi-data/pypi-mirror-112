import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x2vec",
    version="0.0.0",
    author="Baihan Lin",
    author_email="doerlbh@gmail.com",
    description="Python library of word2vec-based similiarity embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doerlbh/x2vec",
    project_urls={
        "Bug Tracker": "https://github.com/doerlbh/x2vec/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    package_dir={"": "x2vec"},
    packages=setuptools.find_packages(where="x2vec"),
    python_requires=">=3.6",
    install_requires=["numpy>=1.16.5", "pandas"],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
)
