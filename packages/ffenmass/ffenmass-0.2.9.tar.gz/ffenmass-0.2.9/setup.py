import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffenmass",
    version="0.2.9",
    author="NoPantsCrash",
    author_email="abtziangiorgos@gmail.com.com",
    description="CLI Utility to encode and recreate directories with ffmpeg.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoPantsCrash/ffenmass",
    project_urls={
        "Bug Tracker": "https://github.com/NoPantsCrash/ffenmass/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    scripts=['bin/ffenmass'],
    install_requires=[
        'setuptools',
        'ffpb',
        'rich',
        'tqdm'
    ],
)
