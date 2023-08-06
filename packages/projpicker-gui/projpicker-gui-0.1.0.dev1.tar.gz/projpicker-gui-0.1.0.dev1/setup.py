import setuptools

with open("README.md") as f:
    long_description = f.read().rstrip()

with open("projpicker-gui/VERSION") as f:
    version = f.read().rstrip()

setuptools.setup(
    name="projpicker-gui",
    version=version,
    license="GPLv3+",
    author="Owen Smith and Huidae Cho",
    author_email="grass4u@gmail.com",
    description="ProjPicker GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HuidaeCho/projpicker-gui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    package_data={"projpicker-gui": ["VERSION"]},
    entry_points={"console_scripts": ["projpicker-gui=gui:main"]},
)
