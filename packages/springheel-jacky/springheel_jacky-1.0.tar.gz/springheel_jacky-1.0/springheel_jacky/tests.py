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

"""Run unit tests."""

import sys, os, json, io, argparse, datetime
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock, call
import springheel_jacky.__main__ as sha
from springheel_jacky import (
    internet,
    links,
    chapters,
    images,
    search,
    strips,
    categories,
    cbz,
)


fakesitejson = {
    "generated_on": 1625467170.160185,
    "springheel_version": "7.0.2",
    "base_url": "https://example.com/springheel/",
    "site_author": "Matthew Ellison",
    "site_author_email": "notarealemail@example.com",
    "language": "en",
    "description": "My awesome Springheel comic!",
    "site_title": "Springheel Comics",
    "country": "United States",
    "site_type": "single",
    "characters_page": False,
    "store_page": False,
    "extras_page": False,
    "license": '<a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="https://example.com/springheel/"><span property="dct:title">Matthew Ellison</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">Sample</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="United States" about="https://example.com/springheel/">United States</span>.',
    "navdirection": "ltr",
    "rename_images": "True",
    "image_rename_pattern": "{comic}_{page}_{titleslug}_{date}.{ext}",
    "zero_padding": "4",
    "site_style": "plain",
    "header_filename": "site_banner.png",
    "social_icons": "False",
    "twitter_handle": "My-Awesome-Springheel-Comic",
    "tumblr_handle": "my-very-awesome-springheeled-comic",
    "patreon_handle": "PatreonDoesNotPubliclyDocumentVanityURLRestrictions-SoICannotConstructADefinitelySafeUnusedExampleURL",
    "liberapay_handle": "awesomespringheeledcomic",
    "pump_url": "https://example.com/pump",
    "diaspora_url": "https://example.com/diaspora",
    "mastodon_url": "https://example.com/mastodon",
    "json_mode": "False",
    "about": "False",
    "archive_page": "https://example.com/springheel/archive.html",
    "categories": [
        {
            "author": "Matthew Ellison",
            "authors": ["Matthew Ellison"],
            "banner": "comic_header.png",
            "bannerw": "512",
            "bannerh": "256",
            "category": "Sample",
            "category_escaped": "Sample",
            "category_theme": False,
            "chapters": True,
            "clicense": "Public domain",
            "conf_c": {
                "category": "Sample",
                "author": "Matthew Ellison",
                "email": "notarealemail@notarealsite.notarealtld",
                "banner": "comic_header.png",
                "header": "site_banner.png",
                "language": "en",
                "mode": "default",
                "status": "in-progress",
                "chapters": True,
                "chars": False,
                "desc": "Example comic for Springheel theme testing.",
                "license": "Public domain",
                "license_uri": "None",
            },
            "desc": "Example comic for Springheel theme testing.",
            "email": "notarealemail@notarealsite.notarealtld",
            "first_page": "0001",
            "header": "site_banner.png",
            "headerh": "256",
            "headerw": "512",
            "known_pages": ["0001"],
            "known_pages_raw": ["1"],
            "known_pages_real": [1],
            "language": "en",
            "last_page": "0001",
            "license_uri": "None",
            "mode": "default",
            "publicdomain": True,
            "slug": "sample",
            "status": "in-progress",
            "strips": [
                {
                    "alt_text": "Example alt text",
                    "author": "Matthew Ellison",
                    "author_email": "notarealemail@notarealsite.notarealtld",
                    "authors": ["Matthew Ellison"],
                    "category": "Sample",
                    "chapter": "1",
                    "commentary": "<p>Commentary goes here.</p>",
                    "copyright_statement": '<p>&copy; 2019&ndash;2021 Matthew Ellison. <a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="https://example.com/springheel/"><span property="dct:title">Matthew Ellison</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">Sample</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="United States" about="https://example.com/springheel/">United States</span>.</p>',
                    "date_fmt": "2019-06-15",
                    "figcaption": "<figcaption>Example alt text</figcaption>",
                    "h1_title": "Sample #1 &ldquo;Page One&rdquo;",
                    "header_title": "Sample #1 &ldquo;Page One&rdquo;",
                    "height": "800",
                    "html_filename": "sample_0001.html",
                    "img": "sample_0001_page-one_2019-06-15.png",
                    "lang": "en",
                    "license": '<a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="https://example.com/springheel/"><span property="dct:title">Matthew Ellison</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">Sample</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="United States" about="https://example.com/springheel/">United States</span>.',
                    "mode": "default",
                    "new_meta": "sample_0001_page-one_2019-06-15.meta",
                    "new_transcr": "sample_0001_page-one_2019-06-15.transcript",
                    "page": "1",
                    "page_padded": "0001",
                    "page_url": "https://example.com/springheel/sample_0001.html",
                    "permalink": '<a href="https://example.com/springheel/sample_0001.html" class="permalink">Permalink</a></p>',
                    "raw_comments": ["Commentary goes here."],
                    "series_slug": "sample",
                    "sha256": "7d62b9a4a1f53a5f240647f26dfc56ebe3ff61210b03153b4892ce460663072f",
                    "slug": "sample_0001",
                    "slugs": ["page-one", "sample"],
                    "statline": '<p class="statline">Sample Page #1 &ldquo;Page One&rdquo; &mdash; Posted by Matthew Ellison, 2019-06-15 &mdash; <a href="pages/sample_0001_page-one_2019-06-15.meta">Metadata (YAML)</a> &mdash; <a href="https://example.com/springheel/sample_0001.html" class="permalink">Permalink</a></p>',
                    "stat_noperma": '<p class="statline">Sample Page #1 &ldquo;Page One&rdquo; &mdash; Posted by Matthew Ellison, 2019-06-15 &mdash; <a href="pages/sample_0001_page-one_2019-06-15.meta">Metadata (YAML)</a> &mdash; <a href="https://example.com/springheel/sample_0001.html" class="permalink">Permalink</a></p><a href="pages/sample_0001_page-one_2019-06-15.meta">Metadata (YAML)</a></p>',
                    "tags": ["example_tag_one", "Example_Tag_Two"],
                    "title": "Page One",
                    "title_slug": "page-one",
                    "tline": "",
                    "transcript_c": "<p>The author has not provided a transcript for this comic.</p>",
                    "width": "600",
                    "url": "https://example.com/springheel/sample_0001.html",
                    "date": "2019-06-15",
                    "year": "2019",
                },
            ],
            "copyright_statement": '<a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="https://example.com/springheel/"><span property="dct:title">Matthew Ellison</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">Sample</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="United States" about="https://example.com/springheel/">United States</span>.',
        }
    ],
    "chapter_info": {"Sample": [{"num": 1, "title": "Sample Chapter"}]},
    "tags": [
        {
            "name": "example_tag_one",
            "url": "https://www.twinkle-night.net/comics/tag-example-tag-one.html",
        },
        {
            "name": "Example_Tag_Two",
            "url": "https://www.twinkle-night.net/comics/tag-example-tag-two.html",
        },
    ],
    "copyright_statement": '<p><a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="https://example.com/springheel/"><span property="dct:title">Matthew Ellison</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">Sample</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="United States" about="https://example.com/springheel/">United States</span>.</p>',
    "site_authors": ["Matthew Ellison"],
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.content = b""
            if status_code == 200:
                self.ok = True
            else:
                self.ok = False

        def json(self):
            return self.json_data

    if (
        args[0] == "https://www.example.com/site.json"
        or args[0]
        == "https://example.com/springheel/pages/sample_0001_page-one_2019-06-15.png"
    ):
        return MockResponse(fakesitejson, 200)

    return MockResponse(None, 404)


class TestConsole(TestCase):
    class MockZipf:
        def __init__(self):
            self.files = [Mock(filename="sample_0001_page-one_2019-06-15.png")]

        def __iter__(self):
            return iter(self.files)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return True

        def infolist(self):
            return self.files

    @patch("requests.get", new=mocked_requests_get)
    def test_retrieve(self):
        """Test site.json extraction."""
        json_data = internet.retrieveJson("https://www.example.com/")
        self.assertEqual(json_data["base_url"], "https://example.com/springheel/")

    def test_chapters(self):
        """Test chapter info extraction."""
        chapterinfo = {"Sample": [{"num": 1, "title": "Sample Chapter"}]}
        fakesitejson = {"chapter_info": chapterinfo, "site_title": "Springheel Comics"}
        self.assertEqual(chapters.getChapters(fakesitejson), chapterinfo)

    # Suppressing print output during tests.
    @patch("sys.stdout", new=io.StringIO())
    def test_nochapters(self):
        """Test chapter info extraction when there are no chapters."""
        fakesitejson = {"site_title": "Springheel Comics"}
        self.assertEqual(chapters.getChapters(fakesitejson), False)

    def test_all_permalinks(self):
        """Test comic permalink retrieval for all categories."""
        self.assertEqual(
            links.getAllPermalinks(fakesitejson),
            [["https://example.com/springheel/sample_0001.html"]],
        )

    def test_cat_permalinks(self):
        """Test comic permalink retrieval for one category."""
        self.assertEqual(
            links.getCatPermalinks(fakesitejson, "Sample"),
            ["https://example.com/springheel/sample_0001.html"],
        )

    def test_chap_permalinks(self):
        """Test comic permalink retrieval for one chapter."""
        self.assertEqual(
            links.getChapPermalinks(fakesitejson, "Sample", 1),
            ["https://example.com/springheel/sample_0001.html"],
        )

    @patch("sys.stdout", new=io.StringIO())
    def test_nonexistent_permalinks(self):
        """Test permalink retrieval for a non-existent category."""
        self.assertEqual(links.getCatPermalinks(fakesitejson, "0"), False)

    def test_all_images(self):
        """Test comic image retrieval for all categories."""
        self.assertEqual(
            images.getAllStrips(fakesitejson),
            [
                [
                    "https://example.com/springheel/pages/sample_0001_page-one_2019-06-15.png"
                ]
            ],
        )

    def test_cat_image(self):
        """Test comic image retrieval for one category."""
        self.assertEqual(
            images.getCatStrips(fakesitejson, "Sample"),
            [
                "https://example.com/springheel/pages/sample_0001_page-one_2019-06-15.png"
            ],
        )

    def test_chap_image(self):
        """Test comic image retrieval for one chapter."""
        self.assertEqual(
            images.getChapStrips(fakesitejson, "Sample", 1),
            [
                "https://example.com/springheel/pages/sample_0001_page-one_2019-06-15.png"
            ],
        )

    def test_dialogue_search(self):
        """Test comic transcript searching."""
        fakesitejson = {
            "categories": [
                {
                    "strips": [
                        {
                            "transcript_c": "<p>The author has not provided a transcript for this comic.</p>",
                            "url": "https://example.com/springheel/sample_0001.html",
                        }
                    ]
                }
            ]
        }
        correct = [
            {
                "transcript_c": "<p>The author has not provided a transcript for this comic.</p>",
                "url": "https://example.com/springheel/sample_0001.html",
            }
        ]
        searchresults = search.searchDialogue(fakesitejson, "transcript")
        self.assertEqual(searchresults, correct)

    def test_tag_search(self):
        """Test comic tag searching."""
        fakesitejson = {
            "categories": [
                {
                    "strips": [
                        {
                            "tags": ["example_tag_one", "Example_Tag_Two"],
                            "url": "https://example.com/springheel/sample_0001.html",
                        }
                    ]
                }
            ],
            "tags": [{"name": "example_tag_one"}, {"name": "Example_Tag_Two"}],
        }
        correct = [
            {
                "tags": ["example_tag_one", "Example_Tag_Two"],
                "url": "https://example.com/springheel/sample_0001.html",
            }
        ]
        searchresults = search.searchTags(fakesitejson, "example_tag_one")
        self.assertEqual(searchresults, correct)

    def test_dialogue_search_noresults(self):
        """Test comic transcript search failure ."""
        fakesitejson = {
            "categories": [
                {
                    "strips": [
                        {
                            "transcript_c": "<p>The author has not provided a transcript for this comic.</p>",
                            "url": "https://example.com/springheel/sample_0001.html",
                        }
                    ]
                }
            ]
        }
        correct = []
        searchresults = search.searchDialogue(fakesitejson, "Nonexistent")
        self.assertEqual(searchresults, correct)

    def test_tag_search_noresults(self):
        """Test comic tag search failure."""
        fakesitejson = {
            "categories": [
                {
                    "strips": [
                        {
                            "tags": ["example_tag_one", "Example_Tag_Two"],
                            "url": "https://example.com/springheel/sample_0001.html",
                        }
                    ]
                }
            ],
            "tags": [{"name": "example_tag_one"}, {"name": "Example_Tag_Two"}],
        }
        correct = []
        searchresults = search.searchTags(fakesitejson, "Nonexistent")
        self.assertEqual(searchresults, correct)

    def test_stripinfo(self):
        """Test comic strip info retrieval."""
        retrieved = strips.getStripInfo(fakesitejson, "Sample", "1")
        correct = "Sample #1 &ldquo;Page One&rdquo;"
        self.assertEqual(retrieved["h1_title"], correct)

    @patch("sys.stdout", new=io.StringIO())
    def test_stripinfo_nonexist(self):
        """Test nonexistent comic strip info retrieval."""
        retrieved = strips.getStripInfo(fakesitejson, "Sample", "5")
        self.assertFalse(retrieved)

    def test_getsite(self):
        """Test URL processing."""
        test = "https://example.com"
        self.assertEqual(internet.getSite(test), "https://example.com/")

    def test_getsite_subdir(self):
        """Test URL processing with a subdirectory."""
        test = "https://example.com/springheel"
        self.assertEqual(internet.getSite(test), "https://example.com/springheel/")

    def test_getsite_subdom(self):
        """Test URL processing with a subdomain."""
        test = "https://springheel.example.com"
        self.assertEqual(internet.getSite(test), "https://springheel.example.com/")

    def test_getsite_fullpage(self):
        """Test URL processing with a full page's URL."""
        test = "https://example.com/springheel/sample_0001.html"
        self.assertEqual(internet.getSite(test), "https://example.com/springheel/")

    @patch("sys.stdout", new=io.StringIO())
    def test_getsite_error(self):
        """Test URL error detection."""
        test = "file:///tmp/springheel"
        self.assertFalse(internet.getSite(test))

    def test_getsite_noprotocol(self):
        """Test URL processing without a protocol."""
        test = "example.com"
        self.assertEqual(internet.getSite(test), "https://example.com/")

    def test_catinfo(self):
        """Test comic category info retrieval."""
        retrieved = categories.getCatInfo(fakesitejson, "Sample")
        correct = "0001"
        self.assertEqual(retrieved["first_page"], correct)

    @patch("sys.stdout", new=io.StringIO())
    def test_catinfo_nonexist(self):
        """Test nonexistent comic category info retrieval."""
        retrieved = categories.getCatInfo(fakesitejson, "Nonexistent")
        self.assertFalse(retrieved)

    @patch("requests.get", new=mocked_requests_get)
    @patch("builtins.open", new=mock_open())
    @patch("os.mkdir", new=mock_open())
    def test_saveimages(self):
        """Test image downloading."""
        status_code = internet.dlImgs(
            [
                "https://example.com/springheel/pages/sample_0001_page-one_2019-06-15.png"
            ],
            "out_dir",
        )
        self.assertEqual(status_code, [200])

    @patch("requests.get", new=mocked_requests_get)
    @patch("springheel_jacky.cbz.zipfile", new=MagicMock(name="zipfile"))
    @patch("sys.stdout", new=io.StringIO())
    def test_dl(self):
        """Test comic downloading."""
        j = fakesitejson
        commands = MagicMock(
            argparse.Namespace, category=None, chapter=None, filename=None
        )
        date = datetime.datetime.strftime(
            datetime.datetime.fromtimestamp(fakesitejson["generated_on"]), "%Y-%m-%d"
        )
        outfile = f"Springheel_Comics_{date}.cbz"
        cbz.createCbzs(j, commands)
        cbz.zipfile.ZipFile.assert_called_once_with(outfile, "w")

    @patch("requests.get", new=mocked_requests_get)
    @patch("springheel_jacky.cbz.zipfile", new=MagicMock(name="zipfile"))
    @patch("builtins.open", new=mock_open())
    @patch("os.mkdir", new=mock_open())
    @patch("shutil.rmtree", new=mock_open())
    @patch("sys.stdout", new=io.StringIO())
    def test_dl_cat(self):
        """Test comic category downloading."""
        j = fakesitejson
        commands = MagicMock(
            argparse.Namespace, category="Sample", chapter=None, filename=None
        )
        outfile = "Sample_0001.cbz"
        cbz.createCbzs(j, commands)
        cbz.zipfile.ZipFile.assert_called_once_with(outfile, "w")

    @patch("builtins.open", new=mock_open())
    def test_comicinfo(self):
        """Test ComicInfo.xml creation."""
        metadata = cbz.constructMeta(
            fakesitejson,
            MagicMock(argparse.Namespace, category=None, chapter=None, filename=None),
            ["springheeljacky_pgstemp/sample_0001_page-one_2019-06-15.png"],
        )
        comicinfo_bytes = cbz.createComicInfo(metadata, "out_dir")
        self.assertEqual(
            comicinfo_bytes.decode(),
            "<?xml version='1.0' encoding='utf8'?>\n<ComicInfo xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><Title>Springheel Comics</Title><Series>Springheel Comics</Series><Summary>My awesome Springheel comic!</Summary><Year>2021</Year><Month>7</Month><Day>5</Day><Writer>Matthew Ellison</Writer><PageCount>1</PageCount><LanguageISO>en</LanguageISO></ComicInfo>",
        )

    @patch("builtins.open", new=mock_open())
    def test_comicinfo(self):
        """Test ComicInfo.xml creation."""
        metadata = cbz.constructMeta(
            fakesitejson,
            MagicMock(argparse.Namespace, category=None, chapter=None, filename=None),
            ["springheeljacky_pgstemp/sample_0001_page-one_2019-06-15.png"],
        )
        comet_bytes = cbz.createCometMeta(metadata, "out_dir")
        self.assertEqual(
            comet_bytes.decode(),
            """<?xml version='1.0' encoding='utf8'?>\n<comet xmlns:comet="http://www.denvog.com/comet/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.denvog.com http://www.denvog.com/comet/comet.xsd"><title>Springheel Comics</title><series>Springheel Comics</series><description>My awesome Springheel comic!</description><date>2021-07-05</date><creator>Matthew Ellison</creator><rights>To the extent possible under law, Matthew Ellison has waived all copyright and related or neighboring rights to Sample. This work is published from: United States.</rights><language>en</language><readingDirection>ltr</readingDirection></comet>""",
        )

    def test_cbzfn(self):
        """Test CBZ filename cleaning."""
        test_meta = {"outname": "Brutus: A Shoujo/ish Webcomic! [Incomplete]"}
        u_fn = None
        self.assertEqual(
            cbz.getFilename(test_meta, u_fn),
            "Brutus_A_Shoujoish_Webcomic_Incomplete.cbz",
        )

    @patch("sys.stdout", new=io.StringIO())
    def test_cbzfn_reserved(self):
        """Test CBZ filename safety."""
        test_meta = {"outname": ""}
        u_fn = "prn.cbz"
        self.assertEqual(cbz.getFilename(test_meta, u_fn), "s_prn.cbz")

    def test_cbzfn_outside(self):
        """Test CBZ filename when outside of current dir."""
        test_meta = {"outname": ""}
        u_fn = "../test.cbz"
        self.assertEqual(cbz.getFilename(test_meta, u_fn), "../test.cbz")

    def test_cbzfn_empty(self):
        """Test CBZ filename when outname is empty."""
        test_meta = {"outname": ""}
        u_fn = None
        self.assertEqual(
            cbz.getFilename(test_meta, u_fn), "Springheel_Comic_Download.cbz"
        )

    def test_cbzfn_toolong(self):
        """Test CBZ filename when outname is too long for Windows."""
        test_meta = {
            "outname": "Fugiat in tempor amet Duis laboris ex qui Excepteur. Sit id consequat nostrud mollit. Consectetur deserunt aute elit. Anim Lorem deserunt culpa in occaecat velit sint elit cupidatat Lorem officia ut. Ut consectetur qui magna non ea, fugiat pariatur ad aliquip officia. Dolor dolore in incididunt elit velit nostrud est.cbz"
        }
        u_fn = None
        self.assertEqual(
            cbz.getFilename(test_meta, u_fn),
            "Fugiat_in_tempor_amet_Duis_laboris_ex_qui_Excepteur__Sit_id_consequat_nostrud_mollit__Consectetur_deserunt_aute_elit__Anim_Lorem_deserunt_culpa_in_occaecat_velit_sint_elit_cupidatat_Lorem_officia_ut__Ut_consectetur_qui_magna_non_ea_fugiat_pariatur_ad_.cbz",
        )

    @patch("sys.stdout", new=io.StringIO())
    def test_cbzfn_toolong_ufn(self):
        """Test CBZ filename when user filename is too long."""
        test_meta = {"outname": ""}
        u_fn = "../Fugiat in tempor amet Duis laboris ex qui Excepteur. Sit id consequat nostrud mollit. Consectetur deserunt aute elit. Anim Lorem deserunt culpa in occaecat velit sint elit cupidatat Lorem officia ut. Ut consectetur qui magna non ea, fugiat pariatur ad aliquip officia. Dolor dolore in incididunt elit velit nostrud est.cbz"
        self.assertEqual(
            cbz.getFilename(test_meta, u_fn),
            "../Fugiat in tempor amet Duis laboris ex qui Excepteur. Sit id consequat nostrud mollit. Consectetur deserunt aute elit. Anim Lorem deserunt culpa in occaecat velit sint elit cupidatat Lorem officia ut. Ut consectetur qui magna non ea, fugiat pariatur ad.cbz",
        )

    @patch("requests.get", new=mocked_requests_get)
    @patch("springheel_jacky.cbz.zipfile", new=MagicMock(name="zipfile"))
    @patch("builtins.open", new=mock_open())
    @patch("os.mkdir", new=mock_open())
    @patch("shutil.rmtree", new=mock_open())
    @patch("sys.stdout", new=io.StringIO())
    def test_cbzfn_cantdelete(self):
        """Test CBZs being put in the temp directory."""
        j = fakesitejson
        outfile = os.path.join("springheeljacky_pgstemp", "Test.cbz")
        commands = MagicMock(
            argparse.Namespace, category="Sample", chapter=None, filename=outfile
        )
        cbz.createCbzs(j, commands)
        # Pages directory is not deleted if the user forced the CBZ
        # to be generated inside it.
        self.assertEqual(cbz.shutil.rmtree.call_count, 0)

    @patch("requests.get", new=mocked_requests_get)
    @patch("builtins.open", new=mock_open())
    @patch("os.mkdir", new=mock_open())
    @patch("sys.stdout", new=io.StringIO())
    def test_saveimages_error(self):
        """Test image downloading error detection."""
        result = internet.dlImgs(
            ["https://example.com/springheel/pages/non-existent.png"],
            "out_dir",
        )
        self.assertFalse(result)
