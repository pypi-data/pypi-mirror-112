import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quickplotlib", # Replace with your own username
    version="0.2.5",
    author="Niccolo Alexander Hamlin",
    author_email="nahamlin@gmail.com",
    description="A wrapper around pandas, matplotlib, and seaborn used to quickly create beautiful viz for analytics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niccoloalexander/quickplotlib",
    project_urls={
        "Bug Tracker": "https://github.com/niccoloalexander/quickplotlib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # py_modules=["quickplot"],
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
    ],
)