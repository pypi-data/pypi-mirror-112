import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
dirParent = "modelingDash"

setuptools.setup(
name="modelingDash", # Replace with your own username
version="1.1.1",
author="Dorian Drevon",
author_email="drevondorian@gmail.com",
description="Utilities package",
long_description=long_description,
long_description_content_type="text/markdown",
# url="https://github.com/pypa/sampleproject",
# project_urls={
#     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
# },
classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
# package_dir={"": dirParent},
# packages=['dorianUtils'],
packages=setuptools.find_packages(),
package_data={'': ['conf/*']},
include_package_data=True,
install_requires=['dorianUtilsModulaire==3.2.3'],
python_requires=">=3.8"
)
