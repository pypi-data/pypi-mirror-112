import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coauction",
    version="0.3",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="This repository contains the source codes of our research paper in economics titled: \"Addictive auctions: using lucky-draw and gambling addiction to increase participation during auctioning\".",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-ravin/collaborative-auction",
    keywords = ['Auctions', 'Auction System', 'Auction Mechanism','Addictive Auctions','Economics'],   # Keywords that define your package best
    install_requires=[        
      ],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


