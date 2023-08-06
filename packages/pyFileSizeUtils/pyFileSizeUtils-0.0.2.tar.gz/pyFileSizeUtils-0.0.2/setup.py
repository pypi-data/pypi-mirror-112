from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
      name='pyFileSizeUtils',
      version='0.0.2',
      description='File size utils contains method for conversion between size unit like byte, kilobyte, megabyte...',
      py_modules=['pyFileSizeUtils'],
      package_dir={'':'src'},
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/xh-dev/pyFileSizeUtils",
      author="xethhung",
      author_email="pypi@xethh.dev",
      extras_require = {
        "dev": [
            "pytest>=3.7",
        ]
      }
)