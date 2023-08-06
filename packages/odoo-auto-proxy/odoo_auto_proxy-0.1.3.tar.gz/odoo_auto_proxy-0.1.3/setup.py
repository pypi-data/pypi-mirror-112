import setuptools
from pathlib import Path

with open(Path(__file__).with_name("requirements.txt"), "r") as fh:
    install_requires = fh.readlines()

setuptools.setup(
    name='odoo_auto_proxy',  
    version='0.1.3',
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="Create Reverse Proxy Configuration For Odoo Containers",
    setup_requires=['setuptools-markdown'],
    install_requires=install_requires,
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/odoo_auto_proxy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)