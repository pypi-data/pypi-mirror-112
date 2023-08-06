import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jevan-library", # Replace with your own username
    version="0.0.20",
    include_package_data=True,
    author="Jevan Solutions",
    author_email="jevan.xtrm@gmail.com",
    description="Core library for each project developed by Jevan Solutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # https://github.com/pypa/sampleproject
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)