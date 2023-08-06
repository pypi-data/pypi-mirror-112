from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="springheel_jacky",
    version="1.0",
    description="Library and command-line interface for Springheel sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
    ],
    keywords="website, webcomic, static",
    url="https://www.twinkle-night.net/Code/springheel_jacky.html",
    author="Garrick",
    author_email="earthisthering@posteo.de",
    license="GPLv3+",
    packages=["springheel_jacky"],
    data_files=[
        ('share/man/man1', ['docs/man/springheel_jacky.1.gz'])
    ],
    install_requires=["requests", "html_text"],
    extras_require={
        "docs": ["sphinx>=3.4.1", "numpydoc"],
    },
    entry_points={"console_scripts": ["springheel_jacky=springheel_jacky.__main__:main"]},
    include_package_data=True,
    zip_safe=False,
)
