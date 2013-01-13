from setuptools import setup, find_packages

setup(
    name='Nanny',
    version='0.1.0',
    author='Andy',
    author_email='andy@eztable.com.tw',
    packages=find_packages(),
    url='http://github.com/andyhorng',
    license='LICENSE.txt',
    description='',
    long_description=open('README.md').read(),
    include_package_data = True,
    install_requires=[
        "pystache",
        "inflection",
        "pyyaml",
        "MySQL-python"
    ],
    entry_points = {
        'console_scripts': [
            'nanny = nanny.app:main'
        ]
    }
)
