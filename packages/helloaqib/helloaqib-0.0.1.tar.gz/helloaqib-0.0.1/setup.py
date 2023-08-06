from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Basic Hello Package'

# Setting up
setup(
    name="helloaqib",
    version=VERSION,
    author="Muhammad Aqib",
    author_email="<inbox.aqib@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)