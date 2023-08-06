import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smModule",
    version="8.1.0",
    author="Pascal Vallaster",
    description="Fixed module-install problem: couldn't install needed modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    install_reqires=["_sqlite3", "platform", "smtplib", "fractions", "colorama", "xml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["sm"],
    package_dir={'': 'sm/src'},
    install_requires=[]
)
