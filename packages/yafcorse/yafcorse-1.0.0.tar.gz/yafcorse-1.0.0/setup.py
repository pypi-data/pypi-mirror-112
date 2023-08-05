from distutils.core import setup

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='yafcorse',
    version='1.0.0',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    url='https://github.com/pyfaddist/yafcorse',
    license='MIT',
    author='Christian Dein',
    author_email='christian.dein@dein-hosting.de',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    description='Yet Another Flask CORS Extension.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
)
