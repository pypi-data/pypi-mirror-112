from setuptools import setup, find_packages

setup(
    name='jsonshower',
    version='2.0.0',
    url='https://github.com/RelevanceAI/jsonviewer',
    author='Jacky Wong',
    author_email='jacky.wong@vctr.ai',
    description='Json Viewer with additional multimedia and highlighting support',
    packages=find_packages(),
    install_requires=['pandas'],
)
