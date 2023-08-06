from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='inltd_lijtool',  # 包名
    version='0.0.1',  # 版本号
    description='A small example package',
    long_description=long_description,
    author='jack lee',
    author_email='983693004@qq.com',
    url='https://xcvu.xyz',
    install_requires=[],
    license='MIT License',
    packages=find_packages(),
    platforms=[
        "all"
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
)