"""Package configuration script."""
from os import path
from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rocket_token",
    version="2.0.1",
    description="Generate tokens for use in the Adzooma platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kieran Lavelle <kieran@clicktech.com>, Michael Brown <michael.b@clicktech.com>",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["cryptography==3.4.7", "click"],
    package_data={
        # If any package contains *.md files include them:
        "": ["*.md"],
    },
    entry_points={
        "console_scripts": [
            "rt_new_keys = rocket_token.cli:generate_keys",
            "rt_web_token = rocket_token.cli:generate_web_token",
            "rt_dev_web_token = rocket_token.cli:generate_developer_web_token",
        ],
    },
)
