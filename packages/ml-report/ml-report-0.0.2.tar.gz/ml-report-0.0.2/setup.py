import pathlib
from setuptools import setup


__version__ = "0.0.2"


here = pathlib.Path(__file__).parent.resolve()


setup(
    name="ml-report",
    version=__version__,
    description="Automated reporting for training and evaluating Machine Learning models",
    long_description=(here / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Wally Wissner",
    author_email="wally.wissner.MS@gmail.com",
    url="https://github.com/wally-wissner/ml_report",
    license=(here / "LICENSE.txt").read_text(),
    install_requires=[
        "eli5 >= 0.11.0",
        "dill >= 0.3.3",
        "joblib >= 1.0.1",
        "nltk >= 3.4",
        "numpy >= 1.18.2",
        "pandas >= 0.25.0",
        "scikit-learn >= 0.24.1",
        "tqdm >= 4.28.1",
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7",
        ]
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: OS Independent",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
    ],
    package_dir={"": "ml_report"},
    python_requires=">=3.7",
)
