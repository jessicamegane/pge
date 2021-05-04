import setuptools

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="core",
    version="0.0.1",
    author="Jessica Mégane",
    author_email="jessicac@student.dei.uc.pt",
    description="Probabilistic Grammatical Evolution Python3 code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jessicamegane/pge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['core'],
    python_requires=">=3.6",
)