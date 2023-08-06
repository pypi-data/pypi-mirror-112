from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt') as f:
        return f.read().split('\n')


def version():
    with open('VERSION') as f:
        return f.read().strip()


setup(
    name='raspi_node',
    author='Mirko Mälicke',
    author_email='mirko@hydrocode.de',
    version=version(),
    install_requires=requirements(),
    packages=find_packages(),
    description='Raspberry Pi based LoRaWAN sensor node base station'
)