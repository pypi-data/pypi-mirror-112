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

from springheel_jacky import internet, links, chapters, images, cli


def main() -> None:
    try:
        commands = cli.getCommands()
    except TypeError:
        return False
    if not commands.url:
        return False
    if not hasattr(commands, "func"):
        return False
    url = internet.getSite(commands.url)
    if not url:
        return False
    j = internet.retrieveJson(url)
    try:
        site_version = j["springheel_version"]
        print(f"Site generated with Springheel {site_version}.")
    except KeyError:
        print("Warning: This site was generated with an old version of Springheel.")
        print("It may not be fully compatible with all features of springheel_jacky.")
    except TypeError:
        print("This is not a Springheel site.")
        return False
    commands.func(j, commands)


if __name__ == "__main__":
    main()
