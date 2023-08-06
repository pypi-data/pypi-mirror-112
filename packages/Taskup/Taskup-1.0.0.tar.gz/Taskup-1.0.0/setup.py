import pathlib
from setuptools import setup

PATH = pathlib.Path(__file__).parent

README = (PATH / "README.md").read_text()

setup(
    name="Taskup",
    version="1.0.0",
    description="A task runner build with Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/haneenmahd/Taskup",
    author="Haneen Mahdin",
    author_email="haneenmahdin@gmail.com",
    include_package_data=True,
    license="MIT",
    scripts=['bin/Taskup.py'],
    entry_points={
        "console_scripts": [
            "Taskup=main:main"
        ]
    }
)