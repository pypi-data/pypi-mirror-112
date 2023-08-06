springheel_jacky man page
=========================

Synopsis
--------

List all links on a site:

    ``springheel_jacky <URL> all_links``

Get image URLs for one chapter:

    ``springheel_jacky <URL> chap_images --category "Foo" --chapter 2``

Get info on chapters:

    ``springheel_jacky <URL> chapters``

Search comic dialogue:

    ``springheel_jacky <URL> search --query "foo"``

Search for a tag:

    ``springheel_jacky <URL> search --tag "foo"``

Get info on one strip:

    ``springheel_jacky <URL> strip --category "Foo" --page 3``

Get info on a category:

    ``springheel_jacky <URL> category --category "Foo"``

Download a comic as CBZ:

    ``springheel_jacky <URL> cbz``

Download a chapter as CBZ:

    ``springheel_jacky <URL> cbz --category "Foo" --chapter 4``

Description
-----------

This is a simple command-line tool to work with Springheel sites without scraping.

When generating a site, Springheel creates a JSON endpoints file; parsing this file allows programs to request resources from the site easily, without mucking around in the HTML. It's not quite an API, but for a static site, it's close enough.

Options
--------

**save** [--filename|-f OUTPUT_FILENAME]

        Download the site.json file to the current directory, for debug purposes.

**chapters**

        List chapter information, if available.

**all_links**

        List permalinks to all comic pages.

**all_images**

        List URLs of all comic image files.

**cat_links** --category|-c CATEGORY_NAME

        List permalinks to comic pages in one category.

**cat_images** --category|-c CATEGORY_NAME

        List URLs of comic image files in one category.

**chap_links** --category|-c CATEGORY_NAME --chapter|-k CHAPTER_NUMBER

        List permalinks to comic pages in one chapter.

**chap_images** --chapter|-k CHAPTER_NUMBER

        List URLs of all comic image files in one chapter.

**search** (--query|-q SEARCH_STRING | --tag|-t TAG)

        Search comic transcripts for a case-insensitive word/phrase, or search for comics with a certain tag (whole word).

**strip** --category|-c CATEGORY_NAME --page|-p PAGE_NUMBER

        Display info on a single strip.

**category** --category|-c CATEGORY_NAME [--no-strips|-n]

        Display info on a single category. Disable appearance of strip info in output with ``--no-strips``.

**cbz** [--category|-c CATEGORY_NAME] [--chapter|-k CHAPTER_NUMBER] [--filename|-f OUTPUT_FILENAME]

        Download a comic as CBZ archive. Defaults to downloading all comics on the site, but can be limited to a single category or chapter if desired.
