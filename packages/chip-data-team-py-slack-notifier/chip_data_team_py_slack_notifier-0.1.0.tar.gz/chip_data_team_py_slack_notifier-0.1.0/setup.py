from setuptools import setup

setup(
    name='chip_data_team_py_slack_notifier',
    version='0.1.0',
    author='Bernard Louis Alecu',
    author_email='louis.alecu@getchip.uk',
    packages=['data_team_py_slack_notifier',],
    #  url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE',
    description="""
	Processes notifications from SNS or custom and sends them to slack.
    """,
    long_description=open('README.md').read(),
    install_requires=[
        "slack_sdk",
	    "pytest",
    ],
)
