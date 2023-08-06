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

"""Show data on chapters."""

import typing


def getChapters(j: dict) -> typing.Union[dict, bool]:
    """
    Try to get chapter info for all comics.

    Parameters
    ----------
    j : dict
        The site JSON contents.

    Returns
    -------
    dict or False
        If existent, a dictionary mapping category names to lists of chapter number: title dictionaries.
    """
    try:
        return j["chapter_info"]
    except KeyError:
        print(f"Comics on {j['site_title']} don't appear to have chapters.")
        return False
