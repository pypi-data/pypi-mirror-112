# The 'setup.py' file

# This file should include 'setuptools.setup()'
# As arguments to that method, we should always pass in:

# 1. name=""
# 2. version=""
# 3. long_description=(
#        can be either {""} OR {Path("README.md")})
# 4. packages=setuptools.find_packages(exclude=[])

# In argument number 4, pass in the names of directories we want
# EXCLUDED from the packages list. They should be pass as strings,
# and separated by a comma.
import setuptools
from pathlib import Path

setuptools.setup(
    name="workwithpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
