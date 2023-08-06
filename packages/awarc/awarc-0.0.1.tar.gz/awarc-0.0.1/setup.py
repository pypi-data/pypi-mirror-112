import setuptools

setuptools.setup(
    name="awarc",
    version="0.0.1",
    author="Anton Wassiljew",
    author_email="anton@wassiljew.online",
    description="tools for working with files archive",
    url="https://github.com/17876/aw-arc.git",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=['setuptools==49.2.0'
                      ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ]
)
