# ctpros: Computed Tomography Processing & Registration - Open Sourced <!-- omit in toc -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![coverage](http://gitlab.com/caosuna/ctpros/-/jobs/artifacts/master/raw/.test_results/coverage.svg?job=coverage)](https://gitlab.com/caosuna/ctpros/-/jobs/artifacts/master/file/.test_results/coverage_html/index.html?job=coverage)

A handy graphic user interface (GUI) and application programming interface (API) to apply common imaging techniques to your research images.

<img src="docs/images/guiexample.png">
Two micro-CT images of a single specimen are shown post-registration of their overlapping region before being stitched.

## Summary <!-- omit in toc -->
This program's goal is to ease the utilization of Python's powerful imaging library in medical imaging research, particularly with micro-computed tomography. By combining raw image data with paired affine matrices to describe their real-world orientations, relationships and scaled metrics can be applied between images of varying resolutions, easing common image processing pipelines. Enabling manipulation of these affine transformations with intuitive dragging and rotating operations allows researchers to better visualize and explore their data.
## Index <!-- omit in toc -->
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Installation
###  Scripts <!-- omit in toc -->
Not familiar with Python? Download and run the following script installer for:
  
- [Windows](bin/ctpros_wininstaller.bat)

  The download button is to the right-most side of the file header:

  ![image-info](docs/images/download_script.PNG)
- Note: Windows may be careful and prompt you to verify to run the script. Select **More Info** then **Run anyway**

  <img src = "docs/images/winsafety.PNG" width=300>


Familiar with Python? Just `pip install ctpros` in your Python 3.7 virtual environment with the below system requirements:
- For all operating systems:
  - [Python 3.7 64-bit](https://www.python.org/downloads/release/python-379/)
    - Development is tested against 3.7.9. Use other versions at your own discretion.
- For headless servers utilizing graphics/graphic commands:
  - `xvfb`
    - X virtual frame buffer to mimic a screen
  - OpenGL
    - Open-sourced graphics library (`libgl1-mesa-dev`)
  
##  Usage
Use either the graphic application for your general visualization and image manipulation needs or use the API for scripting, batching, or specifying pipelines. See below for your use case:

### Graphic User Interface <!-- omit in toc -->
Using one of the installer scripts generates a `ctpros.bat` in the directory of the installer script. Run the generated `ctpros.bat` to call the program.

For those familiar with Python, call `python -m ctpros` from the Python virtual environment in which it is installed.

For detailed controls, see the [GUI Controls Guide](docs/helpme_guicontrols.md).

### Application Programming Interface <!-- omit in toc -->
Import `ctpros` like any other Python module to access the GUI and NumPy-derived image classes. Be sure to use the virtual environment `ctpros` is installed in to be able to import it.
```python
import ctpros

myaim = ctpros.AIM(shape=(50,50,50),dtype='int16')
```
See the [notebooks](notebooks/notebooks.MD) for more examples of API usage.

## Contributors
See [CONTRIBUTING.md](CONTRIBUTING.md) for code requirements and structure, pipeline details, and more.

## License
[GPL 3.0](LICENSE.txt)
