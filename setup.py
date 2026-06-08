from setuptools import setup, find_packages

setup(
    name="devfit",
    version="0.1.0",
    description="Developer Environment Fitness Checker",
    author="DevFit Contributors",
    license="MIT",
    packages=find_packages(),
    py_modules=["devfit"],
    install_requires=["pyyaml>=6.0"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "devfit=devfit:main",
        ],
    },
)
