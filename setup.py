from setuptools import setup

setup(
    name='Spotify Lyrics by dev-mbo',
    author='dev-mbo',
    version='0.0.1',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Session',
        'python-dotenv',
        'requests'
    ],
)