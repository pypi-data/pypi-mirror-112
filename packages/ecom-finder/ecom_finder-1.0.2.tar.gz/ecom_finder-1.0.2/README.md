# Ecom Finder
[![Python package](https://github.com/MYGITHUBPRIYANKA/ecom_finder/actions/workflows/python-package.yml/badge.svg)](https://github.com/MYGITHUBPRIYANKA/ecom_finder/actions/workflows/python-package.yml)

[![Upload Python Package](https://github.com/MYGITHUBPRIYANKA/ecom_finder/actions/workflows/python-publish.yml/badge.svg)](https://github.com/MYGITHUBPRIYANKA/ecom_finder/actions/workflows/python-publish.yml)

<b>Intro</b></br>
This project is can help users to find the optimal solutions for finding best products on ecomerce sites (for ex: amazon, flipkart) based on crawling, AI, Audio Processing, Image Processing, and busines analytics

<b>How To Use</b>

- Installation

  ```
  pip install ecom-finder
  ```

- Useage

  Package Name ecom_finder to import

  ```
    import ecom_finder as ef
    
    # For Text Based Search
    # Parameters - keyword = <Which product we want search online>, nor= <no of products for optimal solutions>
    result = ef.find("iPhone 12", 5)
    for result in result:
        print("-------------------------------------------------------------------------------------------------------------")
        print(result['Product Name'])
        print(result['Ecommerce Provider'])
        print(result['Price'])
        print(result['URL'])
        
    # For Audio Based Search
    # Parameters - nor= <no of products for optimal solutions> , 
    #              device <default=True> Make it false to extract audio from file, if it is False make sure you will provide the correct path for audio_file_path
    #              audio_file_path <default=None> Audio file path that contains the audio input for search ecommerce products
    result = ef.find_by_voice(5)
    for result in result:
        print("-------------------------------------------------------------------------------------------------------------")
        print(result['Product Name'])
        print(result['Ecommerce Provider'])
        print(result['Price'])
        print(result['URL'])
  ```
