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

"""Show data on categories."""

import typing, pprint


def getCatInfo(j: dict, cat_name: str) -> typing.Union[dict, bool]:
    """
    Get information on one category.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    cat_name : str
        The name of the category.

    Returns
    -------
    dict or False
        A dictionary full of information about the category, or False if
        no such category exists.
    """
    base_url = j["base_url"]
    try:
        cat = [item for item in j["categories"] if item["category"] == cat_name][0]
        return cat
    except IndexError:
        print(
            f"""Category {cat_name} not found. Available categories: {"; ".join([item["category"] for item in j["categories"]])}"""
        )
        return False
