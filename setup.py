import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whit-phys-util",
    version="0.1.6.dev2",
    author="John Larkin",
    author_email="jlarkin@whitworth.edu",
    description="Tools to support use of Google Colab + GitHub Classroom for physics lab instruction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnMLarkin/Colab-for-Physics-Lab-Tools",
    install_requires = [
        'pydantic >= 1.7.3',
        'python-dotenv >= 0.10.4',
        'logzero >= 1.6.3'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)