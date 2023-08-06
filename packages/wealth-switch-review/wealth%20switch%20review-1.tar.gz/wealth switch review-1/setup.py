import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 wealth switch review
    name="wealth switch review", # Replace with your own username
    version="1",
    author="wealth switch review",
    author_email="4x0@wealth.com",
    description="wealth switch review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://022254qoyvy04x7gxa50rv8x8s.hop.clickbank.net/?tid=P",
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
