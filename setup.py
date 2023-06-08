from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path)->List:
    """
    get the packages from requirements.txt
    """
    HYPENEDOT = "-e ."
    with open(file_path) as f:
        requirements = f.readlines()
    requirements = [req.replace("\n", "") for req in requirements]
    if HYPENEDOT in requirements:
        requirements.remove(HYPENEDOT)
    return requirements
    




setup(
    name = "mlproject2",
    version = "0.0.1",
    author = "Aniruddh",
    author_email="aniruddhsrm97@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements("requirements.txt")

)
