from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='ttsi',
    version='0.0.7',
    description='Send reports by email',
    long_description=readme,
    author='Dacker',
    author_email='hello@dacker.co',
    url='https://github.com/dacker-team/ttsi',
    keywords='easily send reports email bi data',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3',
    entry_points={
        'console_scripts': ['ttsi=ttsi.__main__:main'],
    },
    install_requires=[
        "rq==1.9.0",
        "Flask==2.0.1",
        "pydatasource==0.2.46",
        "gunicorn==19.7.1",
        "flask-sqlalchemy==2.5.1",
        "flask-admin==1.5.8"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
