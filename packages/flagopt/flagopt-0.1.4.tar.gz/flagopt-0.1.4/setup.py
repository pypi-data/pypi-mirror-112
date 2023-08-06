import setuptools

with open('README.rst') as file:

    readme = file.read()

name = 'flagopt'

version = '0.1.4'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Command line based argument parse framework.',
    long_description = readme,
    install_requires = [
        'multidict'
    ]
)
