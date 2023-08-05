import setuptools, glob, os, sys

version = "0.1.0"
author = "Carlos Osuna"
author_email = "charlie@caosuna.com"
ldct = "text/markdown"
url = "https://gitlab.com/caosuna/ctpros"
dependencies = [
    "itk==4.13.2.post1",
    "layz_import==0.3.2",
    "mayavi==4.6.2",
    "numpy==1.16.5",
    "pandas==0.25.0",
    "scipy==1.6.0",
    "scikit-image==0.17.2",
    "tqdm==4.48.2",
    "xlrd==1.2.0",
    "vtk==8.1.2",
]

setuptools.setup(
    name="ctpros",
    version=version,
    author=author,
    author_email=author_email,
    description="Computed Tomography Processing Registration Open Sourced",
    long_description="# ctpros: Computed Tomography Processing & Registration - Open Sourced\nSee the [project homepage](https://gitlab.com/caosuna/ctpros) for details.",
    long_description_content_type=ldct,
    url=url,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=dependencies,
    python_requires=">=3.7",
)
