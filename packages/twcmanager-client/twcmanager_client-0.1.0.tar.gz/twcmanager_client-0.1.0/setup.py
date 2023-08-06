import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup (
    name='twcmanager_client',
    version='0.1.0',
    author='Jeremy Herbison',
    author_email='jeremy.herbison@gmail.com',
    description='A simple client for communicating with TWCManager',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jherby2k/twcmanager-client',
    project_urls={
        "Bug Tracker": "https://github.com/jherby2k/twcmanager-client/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.7.3"
    ],
)