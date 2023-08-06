import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pidm",
    version="1.0.0",
    author="s0ulix",
    author_email="sombeerjatt@gmail.com",
    description="A module which can download content in parallel threads and increase download speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s0ulix/pidm",
    project_urls={
        "Bug Tracker": "https://github.com/s0ulix/pidm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
