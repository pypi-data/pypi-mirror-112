import os
import re

from setuptools import setup, find_packages
import sys
# 这下面几行是做了小小的封装, 可以先跳过直接看 `setup()` 函数部分
MIDDLEWARE_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

meta_file = open(os.path.join(MIDDLEWARE_BASE_DIR, "testlc", "foo.py")).read()
md = dict(re.findall(r"__([a-z]+)__\s*=\s*'([^']+)'", meta_file))  # 读取 metadata.py 文件

with open(os.path.join(MIDDLEWARE_BASE_DIR, 'README.md')) as f:
    long_description = f.read()

setup(
    name='testlc',
    license='MIT',
    version='0.1',
    description='在这里写对封装的这个包的简单描 述',
    long_description=long_description,  # 详细描述,习惯上内容取自`README.md`文件
    long_description_content_type="text/markdown",
    author='liuchen',
    author_email='1852752478@qq.com',
    url="https://github.com",  # 主页
    download_url='https://github.com',
    packages=find_packages(),
    install_requires=[],
    keywords=['foo'],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)