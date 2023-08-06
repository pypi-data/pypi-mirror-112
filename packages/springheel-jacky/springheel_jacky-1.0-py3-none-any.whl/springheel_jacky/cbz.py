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

#
"""Create CBZ archives from downloaded comics."""

import json, requests, typing, os, zipfile, shutil, datetime, argparse, re
from springheel_jacky import images, internet
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape as xmlescape
import html_text


def createCbzs(j: dict, commands: argparse.Namespace) -> None:
    """
    Download strips from a site and save them as a CBZ archive.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. Optional strings include commands.category
        (to limit results to one category), commands.chapter (to limit
        results to one chapter; does nothing without a category), and
        commands.filename (specifies an output filename).
    """
    cat = True if commands.category else False
    chap = True if commands.chapter else False
    if not cat and not chap:
        imageurls = [item for items in images.getAllStrips(j) for item in items]
    elif cat and not chap:
        imageurls = images.getCatStrips(j, commands.category)
    elif chap and not cat:
        if len(j["categories"]) > 1:
            print("Please specify a category.")
            return False
        else:
            commands.category = j["categories"][0]["category"]
            imageurls = images.getChapStrips(j, commands.category, commands.chapter)
    else:
        imageurls = images.getChapStrips(j, commands.category, commands.chapter)
    if not imageurls:
        print("No comic images found with those criteria. Please try again.")
        return False
    out_dir = "springheeljacky_pgstemp"
    statuscodes = internet.dlImgs(imageurls, out_dir)
    if not statuscodes:
        return False
    image_outs = [os.path.join(out_dir, os.path.basename(img)) for img in imageurls]
    metadata = constructMeta(j, commands, image_outs)
    if not metadata:
        return False
    zip_comment = zipcomment(metadata)
    comicinfo_bytes = createComicInfo(metadata, out_dir)
    image_outs.append(os.path.join(out_dir, "ComicInfo.xml"))
    comet_bytes = createCometMeta(metadata, out_dir)
    image_outs.append(os.path.join(out_dir, "CoMet.xml"))
    out_filename = getFilename(metadata, commands.filename)
    writeCbz(out_filename, image_outs, zip_comment)
    if os.path.abspath(out_dir) not in os.path.abspath(out_filename):
        shutil.rmtree(out_dir)
    else:
        print("The CBZ was created inside the temporary directory. Not deleting.")


def constructMeta(j: dict, commands: argparse.Namespace, imageurls: list) -> dict:
    """
    Construct a metadata dictionary to use as a zip comment.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. Optional strings include commands.category
        (to limit results to one category) and commands.chapter (to
        limit results to one chapter; does nothing without a category).
    imageurls : list of str
        The list of image URLS related to this download. Used to
        estimate page count.

    Returns
    -------
    dict
        A dictionary with information about the downloaded comic.
    """
    meta = {"language": j["language"]}
    date = datetime.datetime.fromtimestamp(j["generated_on"])
    date_f = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S.%f")
    meta["date"] = date_f
    meta["year"] = date.year
    meta["month"] = date.month
    meta["day"] = date.day
    meta["ymd"] = datetime.datetime.strftime(date, "%Y-%m-%d")
    meta["pagecount"] = len(imageurls)
    meta["description"] = j["description"]
    meta["navdirection"] = j["navdirection"]
    meta["license"] = j["license"]
    meta["outname"] = " ".join(
        [j["site_title"], datetime.datetime.strftime(date, "%Y-%m-%d")]
    )
    try:
        authors = set(
            [author for category in j["categories"] for author in category["authors"]]
        )
    except KeyError:
        authors = set(
            [
                author
                for category in j["categories"]
                for strip in category["strips"]
                for author in strip["authors"]
            ]
        )
    meta["authors"] = sorted(list(authors))
    if commands.category:
        meta["series"] = commands.category
        meta["title"] = commands.category
        cat = [
            item for item in j["categories"] if item["category"] == commands.category
        ][0]
        strips = cat["strips"]
        meta["authors"] = sorted(
            list(set([item for authors in strips for item in authors["authors"]]))
        )
        meta["first"] = cat["first_page"]
        meta["last"] = cat["last_page"]
        prange = (
            "-".join([meta["first"], meta["last"]])
            if meta["first"] != meta["last"]
            else meta["first"]
        )
        last_strip = [
            item for item in strips if item["page_padded"] == cat["last_page"]
        ][0]
        date = datetime.datetime.strptime(last_strip["date_fmt"], "%Y-%m-%d")
        meta["date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S.%f")
        meta["ymd"] = datetime.datetime.strftime(date, "%Y-%m-%d")
        meta["year"] = date.year
        meta["month"] = date.month
        meta["day"] = date.day
        meta["outname"] = " ".join([commands.category, prange])
        try:
            meta["license"] = cat["copyright_statement"]
        except KeyError:
            pass
        if j["about"] == "True" and "about" in cat.keys():
            about = (
                html_text.extract_text(cat["about"])
                if "<" in cat["about"]
                else cat["about"]
            )
            meta["description"] = "\n".join([cat["desc"], about])
        else:
            try:
                meta["description"] = cat["desc"]
            except KeyError:
                pass
    else:
        meta["series"] = j["site_title"]
        meta["title"] = j["site_title"]
    if commands.chapter:
        meta["chapter"] = commands.chapter
        strips = sorted(
            [
                item
                for item in cat["strips"]
                if item["chapter"] == str(commands.chapter)
            ],
            key=lambda s: s["page_padded"],
        )
        last_strip = strips[-1]
        date = datetime.datetime.strptime(last_strip["date_fmt"], "%Y-%m-%d")
        meta["date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S.%f")
        meta["ymd"] = datetime.datetime.strftime(date, "%Y-%m-%d")
        meta["year"] = date.year
        meta["month"] = date.month
        meta["day"] = date.day
        try:
            chapter = [
                item
                for item in j["chapter_info"][commands.category]
                if item["num"] == commands.chapter
            ][0]
            pad = len(str(len(j["chapter_info"][commands.category])))
            chpad = f"{commands.chapter:0{pad}d}"
            try:
                meta["title"] = chapter["title"]
                meta["outname"] = " ".join(
                    [commands.category, "ch", chpad, chapter["title"]]
                )
            except KeyError:
                meta["title"] = commands.chapter
                meta["outname"] = " ".join([commands.category, "ch", chpad])
        except KeyError:
            print("This comic isn't divided into chapters.")
            del meta["chapter"]
        except TypeError:
            print(
                "This site's metadata is missing some needed information, so I can't build the CBZ."
            )
            return False
    return meta


def zipcomment(meta: dict) -> str:
    """
    Create a zip comment from metadata.

    Parameters
    ----------
    meta : dict
        A metadata dictionary constructed by :func:`constructMeta()`.

    Returns
    -------
    str
        The zip comment, formatted like ComicTagger.
    """
    zc_d = dict()
    cbinfo = dict()

    cbkeys = [
        "issue",
        "series",
        "credits",
        "comments",
        "publicationYear",
        "tags",
        "title",
        "publicationMonth",
        "publisher",
        "language",
        "genre",
    ]
    if "chapter" in meta.keys():
        cbinfo["issue"] = meta["chapter"]
    cbinfo["series"] = meta["series"]
    cbinfo["credits"] = [
        {"role": "Writer", "person": author} for author in meta["authors"]
    ]
    cbinfo["comments"] = meta["description"]
    cbinfo["publicationYear"] = meta["year"]
    cbinfo["publicationMonth"] = meta["month"]
    cbinfo["title"] = meta["title"]
    cbinfo["language"] = meta["language"]

    zc_d["ComicBookInfo/1.0"] = cbinfo
    zc_d["lastModified"] = datetime.datetime.strftime(
        datetime.datetime.now(), "%Y-%m-%d %H:%M:%S.%f"
    )
    zc_d["appID"] = "Springheel_Jacky"
    return str(zc_d)


def writeCbz(out_fn: str, imagefiles: list, zip_comment: str) -> None:
    """
    Write a CBZ archive.

    Parameters
    ----------
    out_fn : str
        The output filename.
    imagefiles : list of str
        A list of image file paths to add to the zip file.
    zip_comment : str
        A string to use as the zip comment.
    """
    zipf = zipfile.ZipFile(out_fn, "w")
    zipf.comment = zip_comment.encode()
    for file in imagefiles:
        zipf.write(file, os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
    zipf.close()
    print(f"Wrote {out_fn}")


def createComicInfo(meta: dict, out_dir: str) -> str:
    """
    Create a ComicInfo.xml file.

    Parameters
    ----------
    meta : dict
        The metadata to use.
    out_dir : str
        The directory where the XML file should go.

    Returns
    -------
    str
        String containing XML data, for testing purposes.
    """

    root = ET.Element(
        "ComicInfo",
        attrib={
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        },
    )

    ET.SubElement(root, "Title").text = meta["title"]
    ET.SubElement(root, "Series").text = meta["series"]
    if "chapter" in meta.keys():
        ET.SubElement(root, "Number").text = str(float(meta["chapter"]))
    ET.SubElement(root, "Summary").text = xmlescape(meta["description"])
    ET.SubElement(root, "Year").text = str(meta["year"])
    ET.SubElement(root, "Month").text = str(meta["month"])
    ET.SubElement(root, "Day").text = str(meta["day"])
    for writer in meta["authors"]:
        ET.SubElement(root, "Writer").text = writer
    ET.SubElement(root, "PageCount").text = str(meta["pagecount"])
    ET.SubElement(root, "LanguageISO").text = meta["language"]

    tree = ET.ElementTree(root)
    out_fn = os.path.join(out_dir, "ComicInfo.xml")
    tree.write(out_fn, encoding="utf-8", xml_declaration=True)
    # debug
    return ET.tostring(root, encoding="utf8", method="xml", xml_declaration=True)


def createCometMeta(meta: dict, out_dir: str) -> str:
    """
    Create a CoMet-formatted comic metadata file.

    Parameters
    ----------
    meta : dict
        The metadata to use.
    out_dir : str
        The directory where the XML file should go.

    Returns
    -------
    str
        String containing XML data, for testing purposes.
    """
    root = ET.Element(
        "comet",
        attrib={
            "xmlns:comet": "http://www.denvog.com/comet/",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.denvog.com http://www.denvog.com/comet/comet.xsd",
        },
    )
    ET.SubElement(root, "title").text = meta["title"]
    ET.SubElement(root, "series").text = meta["series"]
    if "chapter" in meta.keys():
        ET.SubElement(root, "issue").text = str(meta["chapter"])
    ET.SubElement(root, "description").text = xmlescape(
        html_text.extract_text(meta["description"])
    )
    ET.SubElement(root, "date").text = meta["ymd"]
    for writer in meta["authors"]:
        ET.SubElement(root, "creator").text = writer
    ET.SubElement(root, "rights").text = html_text.extract_text(meta["license"])
    ET.SubElement(root, "language").text = meta["language"]
    ET.SubElement(root, "readingDirection").text = meta["navdirection"]

    tree = ET.ElementTree(root)
    out_fn = os.path.join(out_dir, "CoMet.xml")
    tree.write(out_fn, encoding="utf-8", xml_declaration=True)
    # debug
    return ET.tostring(root, encoding="utf8", method="xml", xml_declaration=True)


def getFilename(metadata: dict, u_fn: typing.Union[str, None]) -> str:
    """
    Safely construct a filename for output.

    Parameters
    ----------
    metadata : dict
        A dictionary providing information about the comic. Should at
        minimum contain the key "outname" with a string value.
    u_fn : str or None
        A user-specified filename, if available.
    """
    windoze_reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    if not u_fn:
        out_slug = re.sub(
            r"(?u)[^-\w.]",
            "",
            str(metadata["outname"]).strip().replace(" ", "_").replace(".", "_"),
        )
        # filename safety
        if not out_slug or set(out_slug) == {"."}:
            out_slug = "Springheel_Comic_Download"
        if out_slug.upper() in windoze_reserved:
            out_slug = f"comic_{out_slug}"
        out_slug = out_slug[0:251]
        out_filename = f"{out_slug}.cbz"
        return out_filename
    else:
        noext, ext = os.path.splitext(u_fn)
        basename_noext = os.path.basename(noext)
        dirpath = os.path.abspath(os.path.dirname(noext))
        if basename_noext.upper() in windoze_reserved:
            print(
                f"""Warning: {basename_noext} is a reserved name on Windows platforms and cannot be used. Adding "s_" for safety."""
            )
            u_fn = os.path.join(dirpath, f"s_{basename_noext}.cbz")
        if len(os.path.basename(u_fn)) >= 255:
            print(f"""Filename {u_fn} is too long. Truncating...""")
            u_fn = os.path.join(dirpath, "".join([basename_noext[0:251], ext]))
        u_fn = os.path.relpath(u_fn)
        return u_fn
