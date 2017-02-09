from setuptools import setup
from setuptools import find_packages


setup(name='src',
      version='1.0.0',
      description='Cool package manager',
      author='Martin Proks',
      author_email='martin.proks@outlook.com',
      url='https://github.com/matq007/src',
      download_url='https://github.com/matq007/src',
      license='MIT',
      packages=find_packages(),

      setup_requires=['requests', 'pytest-runner'],
      tests_require=['pytest'],
      test_suite="src.tests",
      install_requires=['setuptools'],

      include_package_data=True,
      package_data={
          'src': ['packages/*'],
      }
      )

