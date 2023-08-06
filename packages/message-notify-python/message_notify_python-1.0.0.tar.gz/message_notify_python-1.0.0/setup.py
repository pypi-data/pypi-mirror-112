# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

requirements = open('requirements.txt').readlines() # 依赖文件

print(requirements)

setuptools.setup(
    name="message_notify_python",
    version="1.0.0",
    author="alvin",
    author_email="pingtang000@foxmail.com",
    description="message notify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qqingdou/message_notify_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'pycryptodome>=3.10.1',
        'requests>=2.25.1',
    ]
)