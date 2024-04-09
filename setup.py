import os

from setuptools import find_packages, setup

current_directory = os.path.abspath(os.path.dirname(__file__))
print(current_directory)
requirements_path = os.path.join(current_directory, "requirements.txt")
with open(requirements_path, "r") as file:
    requirements = file.read().splitlines()

setup(
    name="liah",
    version="0.1.4",
    author="James Melvin Priyarajan",
    author_email="melvinebenezer@gmail.com",
    description="Insert a Lie in a Haystack and evaluate the model's ability to detect it.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/melvinebenezer/Liah-Lie_in_a_haystack",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    keywords=["llm", "needle in a haystack"],
    python_requires=">=3.6",
    classifiers=[],
    license="Apache 2.0",
)
