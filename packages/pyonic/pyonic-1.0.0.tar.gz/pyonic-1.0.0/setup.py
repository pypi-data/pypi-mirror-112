from setuptools import setup

setup(
    name="pyonic",
    version="1.0.0",
    description="A python SDK for the Ion-Channel application",
    url="https://github.com/ion-channel/ion-channel-python-sdk",
    author="Ion Channel",
    author_email="dev@ionchannel.io",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["Python_SDK"],
    include_package_data=True,
    install_requires=["requests"]
)
