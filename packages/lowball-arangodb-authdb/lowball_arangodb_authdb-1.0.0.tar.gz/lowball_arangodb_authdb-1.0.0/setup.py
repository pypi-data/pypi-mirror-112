from setuptools import setup, find_packages


DESCRIPTION = "An Authentication Database for lowball that uses ArangoDB to store token information"
VERSION = "1.0.0"


def read_requirements():
    """
    Simple helper method to read in the requirements.txt file and parse it into a list for consumption by setuptools
    :return: list of requirements
    """
    required = []
    with open("requirements.txt") as f:
        for line in f:
            if line[0] != "#":
                # Not a comment add it as a requirement
                required.append(line.split("#"))
    return required

def readme():
    """
    Helper to try and format the .md readme file for pretty printing. Falls back to short description.
    :return: The available description
    """
    try:
        import pypandoc
        description = pypandoc.convert_file('README.md', 'rst')
    except:
        description = DESCRIPTION

    return description


setup(name="lowball_arangodb_authdb",
      version=VERSION,
      description=DESCRIPTION,
      long_description=readme(),
      url="https://github.com/EmersonElectricCo/lowball-arangodb-authdb",
      author="Isaiah Eichen",
      author_email="ieichen137@gmail.com",
      license="Apache License 2.0",
      packages=find_packages(),
      install_requires=read_requirements(),
      test_suite="tests",
      zip_safe=False
      )