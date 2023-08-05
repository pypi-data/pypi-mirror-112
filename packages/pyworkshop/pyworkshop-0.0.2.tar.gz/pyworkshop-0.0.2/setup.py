import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyworkshop",
    version="0.0.2",
    author="Yves R. Sagaert",
    author_email="yves.r.sagaert@pm.me",
    license="GNU GPLv3",
    description="A python worskhop package",
    long_description="The package is an example on how to build an release a python package into the wide world.",
    long_description_content_type="text/markdown",
    url="https://github.com/yForecasting/pyworkshop",
    project_urls={
        "Bug Tracker": "https://github.com/yForecasting/pyworkshop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
    ],
    python_requires=">=3.6",
)

