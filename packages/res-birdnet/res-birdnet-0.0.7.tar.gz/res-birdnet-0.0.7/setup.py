import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='res-birdnet',
    version='0.0.7',
    author='Toby Suwindra',
    author_email='tsuwindra@gmail.com',
    description='This model has been trained on Resnet50 and tested on AUC with 93% accuracy. The pretrained model can be accessed on res_birdnet.model_uac93',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tobysuwindra/res-birdnet",
    packages=setuptools.find_packages(),
    install_requires=['torch', 'torchvision'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
