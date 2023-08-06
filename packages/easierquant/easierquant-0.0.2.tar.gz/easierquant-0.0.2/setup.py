# @Author: Tang Yubin <tangyubin>
# @Date:   2021-07-10T11:59:03+08:00
# @Email:  tang-yu-bin@qq.com
# @Last modified by:   tangyubin
# @Last modified time: 2019-05-26T16:26:21+08:00
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easierquant",
    version="0.0.2",
    author="Tang Yubin",
    author_email="tang-yu-bin@qq.com",
    description="a quant tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/aierwiki/easierquant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
