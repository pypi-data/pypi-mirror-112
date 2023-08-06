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

"""Search comics for dialogue for tags."""

import typing
import html_text


def searchDialogue(j: dict, searchstring: str) -> list:
    """
    Search comic transcripts.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    searchstring : str
        The string to search for.

    Returns
    -------
    list
        If not empty, a list of dictionaries for any strips that contain
        matches for the search string.
    """
    results_comics = [
        strip
        for cat in j["categories"]
        for strip in cat["strips"]
        if searchstring.lower() in strip["transcript_c"].lower()
    ]
    sorted_results = sorted(results_comics, key=lambda s: s["url"])
    return sorted_results


def searchTags(j: dict, tag: str) -> list:
    """
    Search comic tags.

    Parameters
    ----------
    j : dict
        The site JSON contents.
    tag : str
        The string to search for.

    Returns
    -------
    list of dict
        If not empty, a list of dictionaries with any strips that are
        tagged with the queried tag.
    """
    # check if tag exists
    if "tags" not in j.keys() or tag not in [item["name"] for item in j["tags"]]:
        return list()
    results_comics = [
        strip
        for cat in j["categories"]
        for strip in cat["strips"]
        if "tags" in strip.keys()
        and tag.lower() in [item.lower() for item in strip["tags"]]
    ]
    sorted_results = sorted(results_comics, key=lambda s: s["url"])
    return sorted_results


def formatResults(results_comics: list, key: str, searchstring: str) -> list:
    """
    Process search results for display in the console.

    Parameters
    ----------
    results_comics : list of dict
        A list of dictionaries representing comic strips, returned by
        one of the search functions.
    key : str
        The type to format the results for. Either "dialogue" or "tags".
    searchstring : str
        The original search string.

    Returns
    -------
    list
        A list of formatted search results.
    """
    if not results_comics:
        print("No results.")
        return list()
    if key == "dialogue":
        results = [
            {
                "url": strip["page_url"],
                "matching": [
                    html_text.extract_text(line)
                    for line in strip["transcript_c"].splitlines()
                    if searchstring.lower() in line.lower()
                ],
            }
            for strip in results_comics
        ]
    elif key == "tags":
        results = [
            {
                "url": strip["page_url"],
                "matching": strip["tags"],
            }
            for strip in results_comics
        ]
    count = len(results)
    results_announce = f"{count} results" if count > 1 else f"{count} result"
    print(results_announce)
    for result in results:
        print(f"URL: {result['url']}")
        print(f"""Matches: {", ".join([f'"{item}"' for item in result["matching"]])}""")
        print("---")
    return results
