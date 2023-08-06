# coding = utf-8
import re
from setuptools import setup, find_packages

with open("yasg_util/__init__.py", "r") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="yasg-util",
    python_requires=">=3.6",
    version=version,
    description="Injecting parameters through annotations based on drf-yasg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="shangsky",
    author_email="t_c_y@outlook.com",
    maintainer="shangsky",
    maintainer_email="t_c_y@outlook.com",
    license="MIT",
    packages=find_packages(),
    platforms=["all"],
    url="https://github.com/ShangSky/yasg-util",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=["drf-yasg"],
)
