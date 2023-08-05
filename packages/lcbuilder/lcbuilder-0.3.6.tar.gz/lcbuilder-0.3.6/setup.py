import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
version = "0.3.6"
setuptools.setup(
    name="lcbuilder", # Replace with your own username
    version=version,
    author="M. Dévora-Pajares",
    author_email="mdevorapajares@protonmail.com",
    description="Easy light curve builder from multiple sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PlanetHunders/lcbuilder",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
    install_requires=['numpy==1.20.1; python_version>="3.7"',
                        'numpy==1.19; python_version<"3.7"',
                        "astropy==4.1",
                        "pandas==1.1.5",
                        "lightkurve==2.0.9",
                        "photutils==1.0.2",
                        "tess-point==0.6.1",
                        "foldedleastsquares==1.0.27"
    ]
)