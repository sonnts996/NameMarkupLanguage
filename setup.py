import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="name_markup_language",
    version="1.0.3",
    author="SonNTS996",
    author_email="sonnts996@gmail.com",
    description="Name Markup Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sonnts996/NameMarkupLanguage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
