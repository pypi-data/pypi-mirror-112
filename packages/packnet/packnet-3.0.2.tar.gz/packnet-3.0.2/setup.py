from setuptools import setup, find_packages



setup(  name = "packnet",
        version = "3.0.2",
        description = "Python3 package for low-level networking",
        long_description = open("README.md").read(),
        long_description_content_type = "text/markdown",
        url = "https://github.com/c0mplh4cks/packnet",
        author = "c0mplh4cks",
        license = "MIT",
        packages = find_packages(),
        python_requires = ">=3",
)
