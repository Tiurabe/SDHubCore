from setuptools import setup, find_packages

setup(
    name='SDHubCore',
    version='0.0.7',
    author='Tiurabe',
    author_email='tiurabe@gmail.com',
    description='Several functions and tools used by SDHub',
    url='https://github.com/tiurabe/SDHubCore',
    packages=find_packages(),
    install_requires=['requests==2.31.0', "pydantic==2.6.0", "colored==2.2.4"],
)
