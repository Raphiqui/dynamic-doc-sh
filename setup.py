from setuptools import setup, find_packages

setup(
    name="dynamic-doc-sh",
    version="0.0.1",
    description="Library to dynamically document sh scripts",
    long_description=open("Usage.md").read(),
    author="Norsse",
    author_email="raphael.pastre@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Jinja2>=3.0",
    ],
    license="MIT",
    python_requires=">=3.12",
)
