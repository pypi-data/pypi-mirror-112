import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
      # pip3 beyond 40 reviews
    name="beyond 40 reviews", # Replace with your own username
    version="1",
    author="beyond 40 reviews",
    author_email="40@beyond.com",
    description="beyond 40 reviews",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hop.clickbank.net/?affiliate=jess1ka&vsl=3&cbpage=text&vendor=beyond40s&tid=py",
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
