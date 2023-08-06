# from typing_extensions import Required
import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cvtoolbox",
    version="0.0.2",
    author="Xudong Shen",
    author_email="sxd95@foxmail.com",
    description="A toolbox that integrates multiple tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xds95/cvtoolbox",
    packages=['cvtoolbox'],
    # packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python',
        'tqdm',
        'imagesize',
        'numpy',
        'imgaug',
        'torch',
        'mmdet'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)