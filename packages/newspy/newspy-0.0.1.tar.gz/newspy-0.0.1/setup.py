import setuptools

setuptools.setup(
    name="newspy",
    version="0.0.1",
    author="Leo Wu-Gomez",
    author_email="leojwu18@gmail.com",
    description="better remake of news-fetch",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
