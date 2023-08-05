from setuptools import setup


packages = ['covid_detection']








setup(name= "covid_detection",

version = "1.0.0",

description = "this a covid detection with audio ml model ",
long_description = "detect covid with audio file ",
author = "Ahmad Dehghani",
author_email = 'ahd76money@gmail.com',
license='MIT',
url = 'https://github.com/jacktamin/king_libs',


packages = packages
,

install_requires = ['librosa'])
