#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright 2021 Matthew "gargargarrick" Ellison <earthisthering@posteo.de>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""Get info on image files."""

import json, requests, sys, typing, pprint


def makeFilename(base_url, img):
    return "/".join(arg.strip("/") for arg in [base_url, "pages", img])


def getAllStrips(j: dict) -> list:
    """
    Get strip images for all comics on the site.

    Parameters
    ----------
    j : dict
        The site JSON contents.

    Returns
    -------
    list of list
        A list of lists -- one for each category -- of comic strip
        image URLs on the site.
    """
    base_url = j["base_url"]
    return [
        sorted([makeFilename(base_url, page["img"]) for page in cat["strips"]])
        for cat in j["categories"]
    ]


def getCatStrips(j: dict, cat_name: str) -> list:
    """
    Get URLs for one category on the site.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    cat_name : str

    Returns
    -------
    list of str
        A list of all comic page URLs in the category.
    """
    base_url = j["base_url"]
    try:
        (cat,) = [item for item in j["categories"] if item["category"] == cat_name]
        return sorted([makeFilename(base_url, page["img"]) for page in cat["strips"]])
    except ValueError:
        print(
            f"""Category {cat_name} not found. Available categories: {"; ".join([item["category"] for item in j["categories"]])}"""
        )
        return False


def getChapStrips(j: dict, cat_name: str, chap_num: int) -> list:
    """
    Get URLs for one chapter.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    cat_name : str
        The name of the category to search.
    chap_num : int
        The chapter number to retrieve pages from.

    Returns
    -------
    list of str
        A list of all comic page URLs in the chapter.
    """
    base_url = j["base_url"]
    try:
        (cat,) = [item for item in j["categories"] if item["category"] == cat_name]
    except ValueError:
        print(
            f"""Category {cat_name} not found. Available categories: {"; ".join([item["category"] for item in j["categories"]])}"""
        )
        return False
    return sorted(
        [
            makeFilename(base_url, item["img"])
            for item in cat["strips"]
            if "chapter" in item.keys() and item["chapter"] == str(chap_num)
        ]
    )
