from setuptools import setup

import fstatemachine

fstatemachine_classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open("README.rst", "r") as fp:
    fstatemachine_long_description = fp.read()

setup(name="fstatemachine",
      version=fstatemachine.__version__,
      author="yakimka",
      author_email="ss.yakim@gmail.com",
      url="https://github.com/yakimka/fstatemachine",
      py_modules=["fstatemachine"],
      description="Python finite state machine",
      long_description=fstatemachine_long_description,
      license="MIT",
      classifiers=fstatemachine_classifiers,
      python_requires=">=3.6",
      )
