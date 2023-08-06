from setuptools import setup, find_packages

setup(
    name='edit_jira',
    version='0.0.7',
    packages=["jira_tool_edit"],

    entry_points={
        "console_scripts": ['JiraE = jira_tool_edit.__main__:main']
    },
    install_requires=[
        "setuptools~=57.1.0",
        "mistletoe~=0.7.2",
        "requests~=2.25.1"
    ],
    url='https://github.com/LogosFu/jira_tool',
    license='GNU General Public License v3.0',
    author='LogosFu',
    author_email='logosfu@gmail.com',
    description='edit markdown file to jira issue',
    python_requires=">=3.6"
)
