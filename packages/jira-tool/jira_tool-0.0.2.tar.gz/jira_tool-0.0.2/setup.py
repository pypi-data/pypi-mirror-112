from setuptools import setup, find_packages

setup(
    name='jira_tool',
    version='0.0.2',
    packages=["jira_tool"],

    entry_points={
        "console_scripts": ['JiraC = jira_tool.__main__:main']
    },
    install_requires=[
        "setuptools~=57.1.0",
        "mistletoe~=0.7.2",
        "requests~=2.25.1"
    ],
    url='https://github.com/LogosFu/jira_tool_create',
    license='GNU General Public License v3.0',
    author='LogosFu',
    author_email='logosfu@gmail.com',
    description='create jira issue from markdown file',
    python_requires=">=3.6"
)
