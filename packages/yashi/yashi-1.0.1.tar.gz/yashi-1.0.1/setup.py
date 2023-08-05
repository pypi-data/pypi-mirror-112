from setuptools import setup

long_description = """\
A placeholder for namespace package `yashi`.
"""

setup(
    name="yashi",
    version="1.0.1",
    description="namespace package for yashihq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=["setuptools>=38.6.0"],  # long_description_content_type support
    author="Qiangning Hong",
    author_email="hongqn@yashihq.com",
    python_requires=">=3.3",  # for native namespace package
    packages=["yashi.emptypackage"],
    extras_require={"dev": ["twine"]},
    zip_safe=False,
    license="MIT",
)
