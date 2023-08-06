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

"""Request resources from the Internet."""

import json, requests, typing, os, asyncio
from urllib.parse import urlparse


def getSite(url: str) -> typing.Union[str, bool]:
    """
    Get the site URL to parse and clean it up a bit.

    Parameters
    ----------
    url : str
        The first argument passed to the command line.

    Returns
    -------
    str or False
        The URL, if it very loosely appears to be a URL. False
        otherwise.
    """
    if not url:
        return False
    url_t = urlparse(url)
    if not url_t.netloc:
        if not url_t.scheme:
            url_t = urlparse(f"https://{url}")
            if not url_t.netloc:
                print(f"{url} doesn't appear to be a URL.")
                return False
        else:
            print(f"{url} doesn't appear to be a URL.")
            return False
    extra = url_t.path
    if ".html" in url_t.path:
        extra = url_t.path.rsplit("/", 1)[0]
    result = os.path.join(
        "{url.scheme}://{url.netloc}{extra}".format(url=url_t, extra=extra), ""
    )
    return result


def retrieveJson(url: str) -> dict:
    """
    Retrieve the JSON endpoints file from a site.

    Parameters
    ----------
    url : str
        The site URL.

    Returns
    -------
    dict
        JSON endpoint data for the site.
    """
    # Get site.json URL
    j_url = "/".join(arg.strip("/") for arg in [url, "site.json"])
    j_r = requests.get(j_url)
    if j_r.ok:
        return j_r.json()
    else:
        print(f"Unable to load endpoint data for {url}")
        return False


# TODO: async
def dlImgs(imagelist: list, out_dir: str) -> list:
    """
    Download images from a list to the specified
    directory.

    Parameters
    ----------
    imagelist : list of str
        A list of image URLs.
    out_dir : str
        The output directory to use. Created if it
        doesn't already exist.

    Returns
    -------
    list
        A list of status codes from the download process (for debug
        purposes).
    """
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    codes = []
    for img in imagelist:
        out_fn = os.path.join(out_dir, os.path.basename(img))
        codes = saveImg(img, out_fn, codes)
    if not codes:
        print("Could not download some comics.")
        return False
    return codes


def saveImg(img: str, out_fn: str, codes: list) -> list:
    """
    Save an image locally.

    Parameters
    ----------
    img : str
        The URL of an image to download.
    out_fn : str
        The output file to save to.
    codes : list
        A list to use for recording status codes.

    Returns
    -------
    list
        A list of HTTP status codes.
    """
    img_req = requests.get(img)
    if img_req.status_code != 200:
        print(f"{img} returned HTTP status code {img_req.status_code}")
        return False
    codes.append(img_req.status_code)
    with open(out_fn, "wb") as image_out:
        imagebytes = img_req.content
        image_out.write(imagebytes)
    return codes
