from setuptools import setup, find_packages
import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(
   name='spi_pack',  # package name
   version='0.3.4',
   description='A module to run analysis',
   url = 'https://github.com/lizahina/test',
   license='MIT',
   author='Elizaveta',
   author_email='ekaduhin@mail.ru',
   packages=find_packages(), #same as name   
   install_requires=[
          'numpy', 'pandas', 'datetime', 'statsmodels', 'seaborn', 'scipy', 'sklearn', 'matplotlib'
           ],
)