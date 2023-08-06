#coding:utf-8
#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="JFP",
    version="0.2",
    keywords=["pip", "zfp", "zip", "jar", "pyZfp", "zfpt", "pyJFP", "jfp"],
    description="A Jar file patch Tool",
    long_description="A Jar file patch Tool",
    long_description_content_type="text/x-rst",
    license="MIT Licence",
 
    url="https://github.com/hexpang/zfp",
    author="HexPang",
    author_email="hexpang@gmail.com",
    entry_points={
        'console_scripts': [
            'zfp = jfp.jfp:main',
            'jfp = jfp.jfp:main'
        ]
    },
 
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
)