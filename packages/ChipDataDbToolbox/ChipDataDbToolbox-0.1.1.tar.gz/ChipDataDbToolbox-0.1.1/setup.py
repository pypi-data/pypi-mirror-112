from setuptools import setup

setup(
    name='ChipDataDbToolbox',
    version='0.1.1',
    author='Bernard Louis Alecu',
    author_email='louis.alecu@getchip.uk',
    packages=['dbToolBox',],
    #  url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE',
    description="""
        Database utility scripts to be reused across projects. 
        Use it to connect to your databases.
    """,
    long_description=open('README.md').read(),
    install_requires=[
        "sqlalchemy",
        "psycopg2",
    ],
)
