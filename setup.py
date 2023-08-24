import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_requirements = {
    "dev": ["wheel", "black", "pytest", "mypy"],
}

setuptools.setup(
    name="AutoReqs",
    version="0.1.3",
    author="Jelte2357",
    author_email="Jelte.dijkmans@gmail.com",
    description="A better way to get the requirements.txt automatically",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            "AutoRequirements=AutoRequirements.AutoRequirements:main",
            "AutoReqs=AutoRequirements.AutoRequirements:main"
        ],
    },
    install_requires=[],
    extras_require=extras_requirements,
    python_requires='>=3.8',
)
