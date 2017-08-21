from setuptools import setup

with open('readme.rst', 'r') as f:
    long_desc = f.read()

setup(
    name='nameko-extension-app',
    version='0.1',
    description='Example app using Nameko extensions',
    author='Anurag Bisht',
    author_email='day.dreamer.web@gmail.com',
    packages=['nameko_extension_app'],
    install_requires=[
        'flask_nameko',
        'nameko_logstash',
        'nameko-sqlalchemy',
        'nameko-redis',
        'Flask',
        'SQLAlchemy',
    ],
)