from setuptools import setup

long_description="Optimizo its an tool that allows to set up instructions and run them later. In the mean you will have to run them manually"

setup(
   name='optimizo',
   version='1.0',
   description='Optimizo its an tool that allows to set up instructions and run them later. In the mean you will have to run them manually',
   license="MIT",
   long_description=long_description,
   author='Takunda Madechangu',
   author_email='madechangu.takunda@gmail.com',
   url="http://taku.co.zw",
   packages=['classes', '.'],  #same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
   
)