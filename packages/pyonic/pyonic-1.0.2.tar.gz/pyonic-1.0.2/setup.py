import setuptools

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setuptools.setup(
    name="pyonic",
    version="1.0.2",
    description="A python SDK for the Ion-Channel application",
    url="https://github.com/ion-channel/ion-channel-python-sdk",
    author="Ion Channel",
    author_email="dev@ionchannel.io",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    py_modules=["client"],
    include_package_data=True,
    install_requires=["requests"]
)
