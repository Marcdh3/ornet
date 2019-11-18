# OrNet
**OrNet** is a Python pipeline for analyzing fluorescence microscopy imagry of mitochondrial protein patterns.

# Dependencies
**Required packages:** scipy, numpy, matplotlib, opencv, itk, cython,
joblib, imageio, scikit-image, scikit-learn, imageio-ffmpeg,
opencv-python>=4

**Python version:**
Python >= 3.7

# Installation
Inside of the root directory of this project run either
`pip install .` or `python setup.py install`

The installation process should install all required dependencies.
However, in the event that not all packages are not installed properly
please refer to the dependicies section and manually instal everything.

# Testing
Inside of the tests subdirectory, run the following command:
`python ornet_tests.py`

All 5 tests should be run without any failures.

# Usage
Ornet can be utilized by calling the Pipeline module from either the command line interface or in a script.
Pipeline will create a directory of the following structure:

outputs/

	singles/

	intermediates/

	distances/

The singles sub-directory will contain the individual videos (.avi) of each extracted cell from the original video, 
intermediates contain compressed numpy files (.npz) that store the means, covariances, weights, and precisions
generated by the gaussian mixture model (GMM) in the pipeline, and the distances directory contains numpy files (.npy)
that represent the divergence metrics between components from the GMM.

## Command Line Interface:
`python -m ornet.Pipeline -i <input video or directory> -m <mask directory> -o <output directory>`

For more detailed information regarding command line options the "-h" flag can be utilized

`python -m ornet.Pipeline -h`

## Python script:
`from ornet import Pipeline as pipeline

pipeline.run(input_path, mask_path, output_path)
`

# Requests, Queries, or Issues
In case of any requested changes, questions, or issues related to this source code please create an issue here.

# Project Status
There is currently no continuous integration set up.

# Publications
If you are using OrNet in a scientific paper, please cite the following:

Bibtex here for scipy paper
Bibtex here for Arxiv entry of thesis

# Overview of Content

# Images
