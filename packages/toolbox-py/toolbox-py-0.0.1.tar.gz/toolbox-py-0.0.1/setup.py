from setuptools import setup, find_packages



setup(
    name="toolbox-py",
    version="0.0.1",
    author="xezzz",
    author_email="ezzz.btw@gmail.com",
    description="A few simple Python utils",
    packages=find_packages(),
    install_requires=["unidecode", "pymongo", "numpy"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)