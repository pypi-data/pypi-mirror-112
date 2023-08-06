from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hns_logicmonitor_api',
    version='21.07.2',
    packages=find_packages(),
    url='https://gitlab.com/horsebridge/hns_logicmonitor_api.git',
    license='MIT',
    author='Nitin Sidhu',
    author_email='nitin.sidhu23@gmail.com',
    description='Logicmonitor API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='~=3.6',
    install_requires=['requests>=2,<3', 'more-itertools>=8.6']
)

