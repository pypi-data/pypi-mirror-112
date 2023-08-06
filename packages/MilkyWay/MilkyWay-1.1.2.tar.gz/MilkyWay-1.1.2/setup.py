from setuptools import setup

setup(
   name='MilkyWay',
   version='1.1.2',
   description='2D Robot trajectory generation',
   author='Hali Lev Ari',
   author_email='LevAri.Hali@gmail.com',
   packages=['milkyway', 'milkyway/splines/'],
   install_requires=['numpy', 'matplotlib'],
)
