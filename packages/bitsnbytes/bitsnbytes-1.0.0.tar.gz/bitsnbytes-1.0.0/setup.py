import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitsnbytes", # Replace with your own username
    version="1.0.0",
    author="Sjoerd Vermeulen",
    author_email="sjoerd@marsenaar.com",
    description="Introduces the Bit, Nibble, Byte and ByteLike types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['bitsnbytes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
