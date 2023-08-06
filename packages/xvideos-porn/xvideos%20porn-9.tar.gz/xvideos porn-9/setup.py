import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 xvideos_porn
    name="xvideos porn", # Replace with your own username
    version="9",
    author="xvideos porn",
    author_email="admin@wow.com",
    description="xvideos porn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.verifysuper.com/cl.php?id=b60b2543a6221b504394eeed6c8ea369",
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
