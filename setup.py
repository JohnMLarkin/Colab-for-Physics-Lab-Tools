import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

exec(open("whit_phys_util/_version.py").read())

setuptools.setup(
    name="whit-phys-util",
    version=__version__,
    author="John Larkin",
    author_email="jlarkin@whitworth.edu",
    description="Tools to support use of Google Colab + GitHub Classroom for physics lab instruction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnMLarkin/Colab-for-Physics-Lab-Tools",
    install_requires = [
        'pydantic >= 1.7.3',
        'python-dotenv >= 0.10.4',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)