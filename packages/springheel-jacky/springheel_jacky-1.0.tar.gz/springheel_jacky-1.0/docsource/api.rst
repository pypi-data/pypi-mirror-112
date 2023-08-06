JSON API
========

This is a listing of the various JSON endpoints exposed to
springheel_jacky.

Site
----

:Keys:

    **about** : str
        Whether or not the comic has an about page.

    **archive_page** : str
        URL of the comic archive page.

    **base_url** : str
        The base URL for this site.

    **categories** : list of dict
        Categories on the site. If single is True, there will only be one entry. See `Categories <#categories>`__ for a list of attributes belonging to these items.

    **chapter_info** : dict
        Information about chapters in each category. See
        `Chapters <#chapters>`__.

    **characters_page** : str or bool
        If it exists, the URL of the characters page.

    **copyright_statement** : str
        HTML-formatted copyright block.

    **country** : str
        The country from which this comic was published. This is mostly relevant if it is public domain.

    **description** : str
        A short description of the site.

    **diaspora_url** : str
        Diaspora* stream URL.

    **extras_page** : str or bool
        If it exists, the URL of the extras page.

    **generated_on** : float
        The date when this site was generated (Unix timestamp).

    **header_filename** : str
        The filename for the site header banner.

    **image_rename_pattern** : str
        The pattern used for renaming images.

    **json_mode** : str
        Whether the site uses JSON files as input or Springheel's original format.

    **language** : str
        The site's language (ISO 639-1 code).

    **liberapay_handle** : str
        Liberapay handle. Applied in the form of ``https://liberapay.com/{liberapay_handle}``

    **license** : str
        An HTML snippet with copyright information on the site.

    **mastodon_url** : str
        Mastodon URL.

    **navdirection** : str
        The metaphorical direction used for navigation arrows. Can be ``ltr`` or ``rtl``.

    **patreon_handle** : str
        Patreon handle. Applied in the form of ``https://www.patreon.com/{patreon_handle}``

    **pump_url** : str
        Pump microblog URL.

    **rename_images** : str
        Whether or not to rename images when building the site.

    **site_author** : str
        The author of this site.

    **site_author_email** : str
        The author's email, used for RSS feed generation. Will probably be fake.

    **site_authors** : list of str
        All persons whose work appears on the site.

    **site_style** : str
        The site theme.

    **site_title** : str
        The overall title of the site.

    **site_type** : str
        Whether the site has multiple "comics" or just one.

    **social_icons** : str
        Whether or not to include social media links on each page.

    **springheel_version** : str
        The version of Springheel used to build the site.

    **store_page** : str or bool
        If it exists, the URL of the store page.

    **tags** : list of dict
        Tags associated with comics. See `Tags <#tags>`__ for available
        attributes.

    **tumblr_handle** : str
        Tumblr blog. Applied like ``https://{tumblr_handle}.tumblr.com``

    **twitter_handle** : str
        Twitter handle. Applied in the form of ``https://twitter.com/{twitter_handle}``.

    **zero_padding** : str
        To how many decimal places comic page numbers should be padded, if any.

Categories
----------

:Keys:


    **category** : str
        The name of the category.

    **characters** : dict
        Character information for this category, if available. See
        `Characters <#characters>`__ for available attributes.

    **copyright_statement** : str
        HTML-formatted copyright block.

    **first_page** : str
        The newest page in the category.

    **known_pages** : list of str
        A list of all zero-padded page numbers in the category.

    **known_pages_raw** : list of str
        A list of all page numbers in the category as they were originally added to Springheel.

    **known_pages_real** : list of int, float, or tuple
        A list of all page numbers in this category converted to integers (or arrays of integers for multi-page spreads).

    **last_page** : str
        The most recent page in the category.

    **strips** : list
        All strips included in this category. See `Strips <#strips>`__ for a list of attributes belonging to these items.

Strips
------

:Keys:


    **alt_text** : str
        A short piece of additional text associated with this strip. Not actually used as alt text.

    **author** : str
        The author of this strip.

    **author_email** : str
        The author's email address. Will probably be fake.

    **authors** : list of str
        All authors listed separately, in case there are more than one.

    **category** : str
        The name of the category associated with this strip.

    **chapter** : str or bool
        The strip's chapter number, if available.

    **commentary** : str
        HTML-formatted commentary on this strip.

    **copyright_statement** : str
        HTML-formatted copyright block.

    **date** : str
        Duplicate of date_fmt

    **date_fmt** : str
        The date on which this strip was published.

    **figcaption** : str
        ``alt_text`` formatted as an HTML figcaption.

    **h1_title** : str
        The strip's title as it appears in the main heading element (with page number and category).

    **header_title** : str
        The same as h1_title.

    **height** : str
        The height of the strip image.

    **html_filename** : str
        An explanation about the purpose of this instance.

    **img** : str
        The filename of the strip image.

    **lang** : str
        The strip's language.

    **license** : str
        An explanation about the purpose of this instance.

    **mode** : str
        Not currently used for anything.

    **new_meta** : str
        The filename of the strip's metadata file.

    **new_transcr** : str
        The filename of the strip's transcript.

    **page** : str
        The strip's page number.

    **page_padded** : str
        The strip's page number, padded with zeroes.

    **page_url** : str
        The strip's URL.

    **raw_comments** : list of str
        The strip's commentary in its original form.

    **series_slug** : str
        The strip's category as a URL slug.

    **sha256** : str
        SHA-256 checksum of the strip image.

    **slug** : str
        The strip's URL slug.

    **slugs** : list of str
        The category and strip title slugs used for file renaming.

    **source** : str
        The URL of a work on which this strip is based, or where it was originally posted.

    **statline** : str
        An HTML block that appears below commentary, listing various metadata about the strip.

    **tags** : list of str
        An optional list of tags associated with this strip.

    **title** : str
        The title of the strip.

    **title_slug** : str
        The title's URL slug.

    **transcript_c** : str
        The HTML block with the strip's transcript.

    **url** : str
        Duplicate of page_url

    **width** : str
        The strip image's width.

    **year** : str
        The year this strip was published.

Characters
----------

The ``characters`` key, if existent, has two keys:

:Keys:

**items** : list of dict
    A list of character items.

**url** : str
    The URL of the resultant characters page.

Each item in the ``items`` list has at minimum the following attributes:

:Keys:

**name** : str
    The character's name.

**desc** : str
    A description of the character.

**img** : str
    An image filename representing a picture of the character.

More attributes may be available depending on the individual site.

Tags
----

:Keys:

**name** : str
    The name of the tag.

**url** : str
    The URL for the tag's index.

Chapters
--------

Keys in this dictionary are the titles of `Categories <#categories>`__.
Each contains a list of dictionaries indicating chapter numbers and, if
available, titles:

:Keys:

**num** : int
    The chapter number.

**title** : str, optional
    The title of the chapter.
