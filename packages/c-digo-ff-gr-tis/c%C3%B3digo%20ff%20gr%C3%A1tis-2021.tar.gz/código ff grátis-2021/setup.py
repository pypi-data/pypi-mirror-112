import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 código ff grátis
    name="código ff grátis", # Replace with your own username
    version="2021",
    author="zcode system",
    author_email="admin@ff.com",
    description="código ff grátis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.verifyspot.net/cl.php?id=6be44989642149752c0cfa865e49ae00",
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
