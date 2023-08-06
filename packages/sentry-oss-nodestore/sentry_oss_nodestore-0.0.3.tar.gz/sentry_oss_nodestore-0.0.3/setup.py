import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentry_oss_nodestore",
    version="0.0.3",
    author="yuanxiao",
    author_email="yuan6785@163.com",
    description="sentry oss node store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # 需要安装的依赖
    install_requires=[
         'oss2==2.14.0',
    ],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[],
)
