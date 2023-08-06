from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3.9"
]
 
setup(
  name="fade",
  version="0.0.1",
  description="This module allows to use Pastebin API very easily.",
  long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
  url="https://github.com/venaxyt/fade",  
  author="Venax",
  author_email="venaxumofficial@gmail.com",
  license="MIT", 
  keywords="fade", 
  classifiers=classifiers,
  install_requires=["requests"],
  packages=["fade"]
)