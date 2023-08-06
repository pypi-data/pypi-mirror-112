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

"""Operate through the command line."""

import sys, argparse, json, pprint, os
from springheel_jacky import links, chapters, images, search, strips, categories, cbz


def pretty_list(l: list) -> None:
    """Pretty-print a list."""
    for i in l:
        print(i)


def chapter_print(cd: dict) -> None:
    """
    Pretty-print a chapter info dictionary.

    Parameters
    ----------
    cd : dict
        A chapter info dictionary.
    """
    for cat, chaplist in cd.items():
        print(f"{cat}:")
        for chap in chaplist:
            print("  Chapter {num}: {title}".format(**chap))


def getCommands() -> argparse.Namespace:
    """
    Extract commands from the command line.

    Returns
    -------
    argparse.Namespace
        Command input.
    """
    parser = argparse.ArgumentParser(prog="springheel_jacky")
    parser.add_argument(
        "url",
        type=str,
        help="The site URL to use.",
    )
    subparsers = parser.add_subparsers(help="Commands to run on the site.")

    parser_save = subparsers.add_parser(
        "save",
        help="Download the site.json file to the current directory, for debug purposes.",
    )
    parser_save.add_argument(
        "--filename",
        "-f",
        type=str,
        help="Output filename (optional).",
    )
    parser_save.set_defaults(func=save_cmd)

    parser_chapters = subparsers.add_parser(
        "chapters", help="List chapter information, if available."
    )
    parser_chapters.set_defaults(func=chapters_cmd)

    parser_all_links = subparsers.add_parser(
        "all_links", help="List permalinks to all comic pages."
    )
    parser_all_links.set_defaults(func=all_links_cmd)

    parser_all_images = subparsers.add_parser(
        "all_images", help="List URLs of all comic image files."
    )
    parser_all_images.set_defaults(func=all_images_cmd)

    parser_cat_links = subparsers.add_parser(
        "cat_links", help="List permalinks to comic pages in one category."
    )
    parser_cat_links.add_argument(
        "--category", "-c", type=str, help="The name of the category to work on."
    )
    parser_cat_links.set_defaults(func=cat_links_cmd)

    parser_cat_images = subparsers.add_parser(
        "cat_images", help="List URLs of comic image files in one category."
    )
    parser_cat_images.add_argument(
        "--category", "-c", type=str, help="The name of the category to work on."
    )
    parser_cat_images.set_defaults(func=cat_images_cmd)

    parser_chap_links = subparsers.add_parser(
        "chap_links", help="List permalinks to comic pages in one chapter."
    )
    parser_chap_links.add_argument(
        "--category", "-c", type=str, help="The name of the category to work on."
    )
    parser_chap_links.add_argument(
        "--chapter", "-k", type=int, help="The number of the chapter to work on."
    )
    parser_chap_links.set_defaults(func=chap_links_cmd)

    parser_chap_images = subparsers.add_parser(
        "chap_images", help="List URLs of all comic image files in one chapter."
    )
    parser_chap_images.add_argument(
        "--category", "-c", type=str, help="The name of the category to work on."
    )
    parser_chap_images.add_argument(
        "--chapter", "-k", type=int, help="The number of the chapter to work on."
    )
    parser_chap_images.set_defaults(func=chap_images_cmd)

    parser_search = subparsers.add_parser(
        "search", help="Search for a comic tag, or search comic transcripts for a case-insensitive word or phrase."
    )
    parser_search.add_argument(
        "--query",
        "-q",
        type=str,
        help="A case-insensitive word or phrase to search for in transcripts.",
    )
    parser_search.add_argument(
        "--tag", "-t", type=str, help="A tag to search for (whole word)."
    )
    parser_search.set_defaults(func=search_cmd)

    parser_strip = subparsers.add_parser(
        "strip", help="Display info on a single strip."
    )
    parser_strip.add_argument(
        "--category", "-c", type=str, help="The name of the strip's category."
    )
    parser_strip.add_argument("--page", "-p", type=str, help="The strip's page number.")
    parser_strip.set_defaults(func=strip_cmd)

    parser_cat = subparsers.add_parser(
        "category", help="Display info on a single category."
    )
    parser_cat.add_argument(
        "--category", "-c", type=str, help="The name of the category."
    )
    parser_cat.add_argument(
        "--no-strips",
        "-n",
        action="store_true",
        help="Omit strips from the category listing (optional).",
    )
    parser_cat.set_defaults(func=cat_cmd)

    parser_cbz = subparsers.add_parser(
        "cbz", help="Download comic as a CBZ archive."
    )
    parser_cbz.add_argument(
        "--category", "-c", type=str, help="The name of the category to save (optional)."
    )
    parser_cbz.add_argument(
        "--chapter", "-k", type=int, help="The number of the chapter to save (optional)."
    )
    parser_cbz.add_argument("--filename", "-f", type=str, help="The output filename (optional).")
    parser_cbz.set_defaults(func=cbz.createCbzs)

    commands = parser.parse_args()
    return commands


def save_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    Save a site.json file locally.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. An optional filename in commands.filename is
        usable but not required.
    """
    out_fn = "site.json"
    if commands.filename:
        a_out_fn = os.path.abspath(commands.filename)
        if os.path.exists(a_out_fn):
            print(f"Could not write to {commands.filename} because it already exists.")
            return False
        else:
            out_fn = a_out_fn
    with open(out_fn, "w") as fout:
        json.dump(j, fout)
    print(f"Wrote {os.path.abspath(out_fn)}")


def chapters_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List chapter information, if available.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input.
    """
    chapterinfo = chapters.getChapters(j)
    if chapterinfo:
        chapter_print(chapterinfo)


def all_links_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List permalinks to all comic pages.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input.
    """
    page_links = links.getAllPermalinks(j)
    pretty_list(page_links)


def all_images_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List URLs of all comic image files.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input.
    """
    page_images = images.getAllStrips(j)
    pretty_list(page_images)


def cat_links_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List permalinks to comic pages in one category.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. A string for command.category is expected.
    """
    page_links = links.getCatPermalinks(j, commands.category)
    pretty_list(page_links)


def cat_images_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List URLs of comic image files in one category.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. A string for command.category is expected.
    """
    page_images = images.getCatStrips(j, commands.category)
    pretty_list(page_images)


def chap_links_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List permalinks to comic pages in one chapter.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. Strings for commands.category and
        commands.chapter are expected.
    """
    page_links = links.getChapPermalinks(j, commands.category, commands.chapter)
    pretty_list(page_links)


def chap_images_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    List URLs of all comic image files in one chapter.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. Strings for commands.category and
        commands.chapter are expected.
    """
    page_images = images.getChapStrips(j, commands.category, commands.chapter)
    pretty_list(page_images)


def search_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    Search comic transcripts for a case-insensitive word or phrase.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. A string for either commands.query or
        commands.tag is expected.
    """
    if commands.query and commands.tag:
        print(
            "Currently, you can only search for either dialogue or a tag at one time."
        )
        return False
    else:
        if commands.query:
            results = search.searchDialogue(j, commands.query)
        else:
            results = search.searchTags(j, commands.tag)
    if results:
        count = len(results)
        results_announce = f"{count} results" if count > 1 else f"{count} result"
        print(results_announce)
        sorted_results = sorted(results, key=lambda s: s["url"])
        for result in sorted_results:
            print(f"URL: {result['url']}")
            print(
                f"""Matches: {", ".join([f'"{item}"' for item in result["matching"]])}"""
            )
            print("---")


def strip_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    Display info on a single strip.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. Strings for commands.category and
        commands.page are expected.
    """
    info = strips.getStripInfo(j, commands.category, commands.page)
    pprint.pprint(info)


def cat_cmd(j: dict, commands: argparse.Namespace) -> None:
    """
    Display info on a single category.

    Parameters
    ----------
    j : dict
        Site JSON contents.
    commands : argparse.Namespace
        Command input. A string for commands.category is expected. An
        optional bool for commands.no_strips removes the ``strips`` key
        from output.
    """
    info = categories.getCatInfo(j, commands.category)
    if commands.no_strips:
        del info["strips"]
    pprint.pprint(info)
