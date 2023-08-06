import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 porn_downloader
    name="porn downloader", # Replace with your own username
    version="2021",
    author="porn downloader",
    author_email="admin@wopw.com",
    description="porn downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.verifysuper.com/cl.php?id=506a54793a9fc50278eec56be3657436",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
