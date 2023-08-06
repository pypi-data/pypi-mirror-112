# Third party imports
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='ecom_finder',
      version='1.0.2',
      description='Python based library to find any product in ecommerce site using crawling and AI (like audio, images)',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/MYGITHUBPRIYANKA/ecom_finder',
      author='Priyanka Das',
      author_email='mymailid.priyanka@gmail.com',
      license='MIT License',
      packages=['ecom_finder'],
      include_package_data=True,
      install_requires=["bs4", "pandas", "requests", "SpeechRecognition", "pyaudio"],
      zip_safe=False)
