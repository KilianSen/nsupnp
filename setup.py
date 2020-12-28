import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nsupnp", # Replace with your own username
    version="1.0.0",
    author="Kilian Senger",
    author_email="kilian@senger.group",
    description="A small custom upnp implementation inspired by the real one",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://senger.group/ks/networking/nusupnp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)