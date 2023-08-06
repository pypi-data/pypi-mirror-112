from setuptools import setup, Extension

setup(
    name="turbodict",
    version="0.1.0",
    description="Cool dict extensions.",
    author="Frank Smit",
    author_email="frank@61924.nl",
    url="https://git.sr.ht/~fsx/turbodict",
    license="MIT",
    packages=["turbodict"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    ext_modules=[Extension("turbodict._attrdict", sources=[
        "turbodict/_attrdict.c",
    ])],
)
