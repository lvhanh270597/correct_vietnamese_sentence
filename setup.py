import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vicorrect",
    version="0.0.1",
    author="Hanh.Le Van",
    author_email="lvhanh.270597@gmail.com",
    description="Helpful tool to guess correct vietnamese sentence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvhanh270597/correct_vietnamese_sentence",
    packages=setuptools.find_packages(),
    install_requires=[
        'nltk'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)