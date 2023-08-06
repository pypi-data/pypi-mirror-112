from setuptools import setup

with open("README.md", 'r') as fileobj:
    long_description = fileobj.read()

setup(
   name='optimizo',
   version='1.3',
   description='Optimizo its an tool that allows to set up instructions and run them later. In the mean you will have to run them manually',
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Takunda Madechangu',
   author_email='madechangu.takunda@gmail.com',
   url="http://taku.co.zw",
   packages=['classes', '.'],  #same as name
   install_requires=[
       'appdirs==1.4.4',
        'autopep8==1.5.7',
        'css-html-js-minify==2.5.5',
        'distlib==0.3.2',
        'filelock==3.0.12',
        'pycodestyle==2.7.0',
        'six==1.16.0',
        'tinydb==4.5.0',
        'toml==0.10.2',
        'virtualenv==20.4.7',
        'virtualenvwrapper-win==1.2.6',
   ], #external packages as dependencies
   
)