#setup.py
from setuptools import setup
import re

#change version number in ngrok_server file  add/edit version="DESIRED_VERSION NUMBER" at the top of file

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('ngrok_server').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"


setup(
    name='ngrok_server',
    scripts=['ngrok_server'],
    version= version,
    description = 'simple project, simple life',
    long_description = long_descr,
    author = 'madhavth'
)
