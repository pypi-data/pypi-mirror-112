import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typed_configurator",
    version="0.0.1",
    author="Lee",
    author_email="keqianlimail@gmail.com",
    description="A small configurator library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kleeeeea/configurator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
