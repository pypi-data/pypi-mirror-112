from setuptools import find_packages, setup

setup(
    name='nascorp.library',
    version='0.1.0',
    description='Nascorp Library',
    author='NASCORP TECHNOLOGY',
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)
