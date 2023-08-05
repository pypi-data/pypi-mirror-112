import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name = "Bold-Falcon",
    version = "0.0.1",
    author = "PowerLZY",
    author_email = "3289218653@qq.com",
    description = "毕方智能云沙箱(Bold-Falcon)是一个开源的自动化恶意软件分析系统",
    long_description_content_type = "text/markdown",
    long_description = long_description,
    url = "https://github.com/PowerLZY/Bold-Falcon",
    packages = setuptools.find_packages(),
    classifers = [
    "Programming Language :: Python :: 2.7",
    "Liense :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]

)