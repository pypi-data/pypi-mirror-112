from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()


setup(
  name = 'exurl',
  packages = ['exurl'],
  version = '1.2.01',
  license='MIT',
  description = 'Division url to many urls approval on parameters - to make fuzzing or testing parameters one by one',
  author = 'Abdulrahman Kamel',
  author_email = 'vulnabdo@gmail.com',
  url = 'https://github.com/Abdulrahman-Kamel/exurl',
  long_description_content_type="text/markdown",
  long_description = long_description,
  #download_url = 'https://github.com/Abdulrahman-Kamel/exurl/archive/pypi-0_1_3.tar.gz',
  #keywords = ['split', 'easy', 'scraper', 'website', 'download', 'links', 'images', 'videos'],
  install_requires=['urllib3>=1.25.9']
)