from setuptools import setup, find_packages

setup(
    name="linksnake",
    version="1.0",  
    py_modules=["linksnake"],
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "playwright",
        "lxml",
        "requests",
    ],
    entry_points={
      "console_scripts": [
        "linksnake = linksnake:entry_point",
      ],
    },
    author="Napol Thanarangkaun",
    description="A simple web crawler using Python and Playwright",
)
