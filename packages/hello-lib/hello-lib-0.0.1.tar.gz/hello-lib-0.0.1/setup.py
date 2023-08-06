import setuptools

with open("README_pdapi.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hello-lib",  # Replace with your own username
    version="0.0.1",
    author="Nancykhullar",
    author_email="nancy.khullar97@gmail.com",
    description="A lib to do the initial testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas==1.1.4',
        'firebase-admin==4.4.0',
        'pyarrow==2.0.0',
    ]
)
