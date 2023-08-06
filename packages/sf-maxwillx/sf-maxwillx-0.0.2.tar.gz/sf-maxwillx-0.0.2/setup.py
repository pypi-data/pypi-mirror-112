import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sf-maxwillx",
    version="0.0.2",
    author="Max Willx",
    author_email="maxwillx@gmail.com",
    description="a simple subtitle name formater",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['sfcmd=sf.entry:main'],
    }
)
