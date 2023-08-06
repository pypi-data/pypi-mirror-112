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

"""Get info on individual strips."""

import typing, pprint


def getStripInfo(j: dict, cat_name: str, page_num: str) -> dict:
    """
    Get information on one strip.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    cat_name : str
        The name of the strip's category.
    page_num : str
        The page number. Leading zeroes are stripped.

    Returns
    -------
    dict
        A dictionary full of information about the strip.
    """
    base_url = j["base_url"]
    if set(page_num) != {"0"}:
        noz = page_num.lstrip("0")
    else:
        noz = "0"
    try:
        cat = [item for item in j["categories"] if item["category"] == cat_name][0]
    except IndexError:
        print(
            f"""Category {cat_name} not found. Available categories: {"; ".join([item["category"] for item in j["categories"]])}"""
        )
        return False
    try:
        page = [item for item in cat["strips"] if item["page"] == noz][0]
        return page
    except IndexError:
        print(
            f"""Page #{noz} not found. Available page numbers in category {cat_name}: {", ".join([item["page"] for item in sorted(cat["strips"], key=lambda s: s["page_padded"])])}"""
        )
        return False
