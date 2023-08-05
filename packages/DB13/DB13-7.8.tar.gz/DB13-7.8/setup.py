import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DB13",
    description="DIRAC Benchmark 2012",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/DIRACGrid/DB12",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    project_urls={
        "Bug Tracker": "https://github.com/pypa/DIRACGrid/DB12/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=2.7",
    entry_points={
    'console_scripts': [
        'db12 = DIRACbenchmark.dirac_benchmark:main',
    ],
},
)
