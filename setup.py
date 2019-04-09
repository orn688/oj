from setuptools import find_namespace_packages, setup

setup(
    name="oj",
    version="0.1",
    description="Oliver's JSON parser",
    url="http://github.com/orn688/oj",
    author="Oliver Newman",
    author_email="orn688@gmail.com",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
)
