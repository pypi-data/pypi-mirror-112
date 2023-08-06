from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="FastTelethonhelper",
    version="0.0.1",
    description="Make Telethon files upload/download faster",
    package_dir={'': 'FastTelethonhelper'},
    install_requires=["telethon", "telethon-tgcrypto", "cryptg"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MiyukiKun/FastTelethonhelper",
    author="MiyukiKun",
    author_email="hardikmajethia9529@gmail.com"

)