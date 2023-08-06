import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as f:
    long_description = f.read()

setuptools.setup(
    name="MangasOrigines",
    version="0.0.3",
    author="Asthowen",
    author_email="contact@asthowen.fr",
    license="GNU v3.0",
    description="A script for download scans on https://mangas-origines.fr/ written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Asthowen/MangasOriginesDownloader",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ['mangas_origines = mangas_origines.mangas_origines:start']
    },
    python_requires='>= 3.6',
    include_package_data=True,
    install_requires=['aiohttp', 'aiofiles', 'bs4']
)
