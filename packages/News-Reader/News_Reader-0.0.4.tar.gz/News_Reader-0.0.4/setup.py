from setuptools import setup
classifiers  = [
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python :: 3',
]
setup(name = "News_Reader",
version = "0.0.4",
description = """This Is A Indian News reader Program Devloped By Parth Arora To Impress Your Friends
""",
long_description = f"""{open("README.md").read()}\n\n{open("CHANGELOG.txt").read()}
""",  
classifiers = classifiers,
packages = ['News-Reader'],
keywords = "news reader",
install_requires = ["pywin32"],
author = "Parth Arora",
license = "MIT",
) 