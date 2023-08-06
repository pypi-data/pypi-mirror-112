#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Priyanka Das
# @Version : 1.0.1
#
# ecom_finder

# Standard library imports
import re as __re__
import urllib as __ulp__

# Third party imports
import pandas as __pd__
import requests as __requests__
import speech_recognition as __sr__
from bs4 import BeautifulSoup as __BS__


# Get items list From amazon.in
# Inputs: text (Item Name)
# Outputs: pandas dataframe of items
def __get_items_from_amazon__(text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    query = "https://www.amazon.in/s?" + __ulp__.parse.urlencode({"k": text.lower()})
    code = __requests__.get(query, headers=headers)
    s = __BS__(code.text, "html.parser")
    items = s.findAll("div", attrs={"class": "a-section"})
    alls = []
    for item in items:
        name = item.find(
            "span", attrs={"class": "a-size-medium a-color-base a-text-normal"}
        )
        price = item.find("span", attrs={"class": "a-price-whole"})
        url = item.find("a", attrs={"class": "a-link-normal a-text-normal"})
        rating = item.find("span", attrs={"class": "a-icon-alt"})

        if name == None or price == None:
            continue
        else:
            alls.append(
                {
                    "name": name.text,
                    "price": price.text,
                    "url": "https://amazon.com" + url["href"]
                    if url.has_attr("href")
                    else None,
                    "rating": float(rating.text.split(" ")[0])
                    if rating is not None
                    else None,
                    "provider": "Amazon",
                }
            )
    return __pd__.DataFrame(alls)


# Get items list From flipkart.in
# Inputs: text (Item Name)
# Outputs: pandas dataframe of items
def __get_items_from_flipkart__(text):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    query = "https://www.flipkart.com/search?" + __ulp__.parse.urlencode(
        {"q": text.lower()}
    )

    code = __requests__.get(query, headers=headers)
    soup = __BS__(code.text, "html.parser")

    alls = []

    for item in soup.select("[data-id]"):
        try:
            alls.append(
                {
                    "name": item.select("a img")[0]["alt"],
                    "price": float(
                        item.find_all(text=__re__.compile("₹"))[0]
                        .replace("₹", "")
                        .replace(",", "")
                    ),
                    "provider": "Flipkart",
                    "rating": float(
                        item.select("[id*=productRating]")[0].get_text().strip()
                    ),
                    "url": "https://flipkart.com" + item.select("a")[0]["href"],
                }
            )

        except Exception as e:
            continue

    return __pd__.DataFrame(alls)


# Get best items
# Inputs: keyword, number of results
# Outputs: json formatted output based on analysis
def find(keyword, nor=10):
    # Find Products From E-commerce sites
    amazon = __get_items_from_amazon__(keyword)
    flipkart = __get_items_from_flipkart__(keyword)

    # Analise data & send top 10 results
    data = __pd__.concat([amazon, flipkart], sort=True)

    def __find_by_name__(keyword, name):
        __name__ = name.lower().strip()
        __keyword__ = keyword.lower().strip()
        if __name__ == __keyword__:
            return 0
        elif __name__.startswith(__keyword__):
            return 1
        elif __keyword__ in __name__:
            return 2
        else:
            return None

    data["rank"] = data.name.apply(lambda x: __find_by_name__(keyword, x))

    return (
        data[(~data["rank"].isna()) & (~data["rating"].isna())]
        .drop_duplicates()
        .sort_values(["rank", "rating"], ascending=[True, False])
        .reset_index(drop=True)[:nor][["name", "price", "provider", "url"]]
        .rename(
            columns={
                "name": "Product Name",
                "price": "Price",
                "url": "URL",
                "provider": "Ecommerce Provider",
            }
        )
        .to_dict(orient="records")
    )


# Get best items by voice
# Inputs: audio_file_path / device, number of results
# Outputs: json formatted output based on analysis
def find_by_voice(nor=10, device=True, audio_file_path=None):

    if device == False:
        f = __sr__.AudioFile(audio_file_path)
        r = __sr__.Recognizer()
        with f as source:
            audio = r.record(source)
    else:
        r = __sr__.Recognizer()
        with __sr__.Microphone() as source:
            print("Are you looking for...")
            audio = r.listen(source)

    instructions = r.recognize_google(audio)
    print("You are looking for ...", instructions)
    return find(instructions, nor)


# Get best items by image
# Inputs: image_file_path, number of results
# Outputs: json formatted output based on analysis
def find_by_image(image_file_path, nor=10):
    print("Available in next version, use find() instead...")
