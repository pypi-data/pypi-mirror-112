from setuptools import setup, find_packages

setup(name='appmath',
      version='0.0.1',
      url='https://github.com/aogavrilov/appmath',
      license='MIT',
      author='Alexey Gavrilov',
      author_email='alexgavrilov28@gmail.com',
      description='Some methods of numerical mathematics which support calculation on GPU',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)