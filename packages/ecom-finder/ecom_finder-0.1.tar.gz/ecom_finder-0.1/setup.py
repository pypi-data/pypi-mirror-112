# Third party imports
from setuptools import setup

setup(name='ecom_finder',
      version='0.1',
      description='Python based library to find any product in ecommerce site using crawling and AI (like audio, images)',
      url='https://github.com/MYGITHUBPRIYANKA/ecom_finder',
      author='Priyanka Das',
      author_email='mymailid.priyanka@gmail.com',
      license='MIT License',
      packages=['ecom_finder'],
      include_package_data=True,
      install_requires=["bs4", "pandas", "requests", "re", "urllib", "SpeechRecognition", "pyaudio"],
      zip_safe=False)
