from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    README_MD = fh.read()

setup(
    name="symmetrypy",
    version="0.1.5",
    description=""" Solana RPC API for symmetry """,
    long_description=README_MD,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aiohttp'
    ],
    python_requires=">=3.8, <4",
    keywords="symmetry blockchain solana",
    packages=find_namespace_packages(exclude=["tests", "tests.*", "venv", "venv.*"]),
    classifiers=[
        "Development Status :: 1 - Planning",
    ]
)