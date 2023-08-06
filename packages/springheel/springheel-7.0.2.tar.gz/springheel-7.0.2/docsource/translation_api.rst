Translation API
===============

These are the default translation string keys in ``strings.json``, as
well as how they're used.

about_s
  ``About``

  Used in top navigation.

all_pages_s
  ``All Pages in Chapter {chapter}``

  Used on archives to mark the chapter-view page for a chapter.

alt_chapter_s
  ``<a href="{ch_outfn}">{category} {chapter_s}</a>, Page #{page} &ldquo;{title}&rdquo;``

  Used on the meta line if the chapter doesn't have a title.

alt_nochapter_s
  ``{category} Page #{page} &ldquo;{title}&rdquo;``

  Used on the meta line if the comic doesn't have chapters.

archive_l_s
  ``#{page} &ldquo;{title}&rdquo;``

  String used for linking on the archive page.

archive_s
  ``Archives``

  Used in top navigation.

caption_s
  ``Commentary``

  Heading used on comic and chapter-view pages.

category_chapter_s
  ``{category} {chapter_s}``

  The category and ``chapter_s`` combined. Used for the archive table of contents and headings on chapter-view pages.

cc
  ``<span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/StillImage" property="dct:title" rel="dct:type">{category}</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="{base_url}" property="cc:attributionName" rel="cc:attributionURL">{author}</a> is licensed under a <a rel="license" href="{license_uri}">{clicense} License</a>.``

  HTML block for Creative Commons licensing.

  Only used on libre comics.

ccpdw
  ``<a rel="license" href="http://creativecommons.org/publicdomain/zero/1.0/"></a>To the extent possible under law, <a rel="dct:publisher" href="{site_url}"><span property="dct:title">{author}</span></a> has waived all copyright and related or neighboring rights to <span property="dct:title">{site_title}</span>. This work is published from: <span property="vcard:Country" datatype="dct:ISO3166" content="{author_country}" about="{site_url}">{author_country}</span>.``

  Statement used to waive copyright.

  Only used on public domain comics.

chapbook_meta_link_s
  ``Page #{page} Metadata ({file_ext})``

  Used in WAI-ARIA labels on chapter view pages, so that metadata links are unambiguous. Visible only to screen readers.

chapbook_page_alt_s
  ``Comic Page #{page}``

  Used as alt text for page images on chapter view pages.

chapbook_source_s
  ``Page #{page} Source``

  Used in WAI-ARIA labels for statlines, to make the context of “source” more obvious. Visible only to screen readers.

chapbook_transcript_link_s
  ``Page #{page} Transcript ({file_ext})``

  Used in WAI-ARIA labels on chapter view pages, so that transcript links are unambiguous. Visible only to screen readers.

chapter_s
  ``Chapter {chapter}: {chapter_title}``

  Used on archive pages and for constructing other chapter strings.

char_s
  ``Characters``

  Used in top navigation.

complete_s
  ``Complete``

  Status displayed on the index and archive.

date_format
  [``"-"``, ``"-"``, ``""``]

  List of strings used in conjunction with `strf_format`, corresponding to ``y``, ``m``, ``d``, respectively. Each element is interleaved with the date format, so you can put things after the month, day, and year numbers.

decimal_separator
  ``.``

  The mark used as a decimal separator in fractional pages.

extra_s
  ``Extras``

  Used in top navigation.

first_s
  ``First (#{page})``

  Alt text for page navigation. Formatted with a page number.

firstch_s
  ``First Chapter ({page})``

  Chapter navigation button alt text. Formatted with a chapter number.

firsts_s
  ``First``

  Showed below navigation arrow.

firstsch_s
  ``First``

  Showed below navigation arrow on chapter-view pages.

  Separate from the regular page version because "page" and "chapter" have different grammatical genders in some languages.

generator_s
  ``Built with <a href="https://www.twinkle-night.net/Code/springheel.html">Springheel</a> {version}.``

  Springheel advertisement showed on all pages.

goarchive_s
  ``Go to archive``

  Used on the index page.

gofirst_s
  ``Go to first page``

  Used on the index page.

golatest_s
  ``Go to latest page``

  Used on the index page.

h1_s
  ``{category} #{page} &ldquo;{title}&rdquo;``

  Title used for heading elements and meta tags.

hiatus_s
  ``On hiatus``

  Status displayed on the index and archive.

home_s
  ``Home``

  Used in top navigation.

image_s
  ``Image`` ``:`` 

  Used on extra pages.

  The English default is actually "Image: " with the space after the colon, but restructuredText does not like that.

inprogress_s
  ``In-progress``

  Status displayed on the index and archive.

jsonfeed_descr
  ``This feed allows you to read the posts from this site in any feed reader that supports the JSON Feed format. To add this feed to your reader, copy the following URL—{jsonfeedurl}—and add it your reader.``

  Description used in JSON Feeds.

jsonfeed_name
  ``JSON Feed``

  JSON Feed icon alt text.

language_names

  A sub-dictionary mapping various ISO 639-1 language codes to their names in their respective language (e.g. de: Deutsch). Used for multi-language site links.

last_s
  ``Last (#{page})``

  Alt text for page navigation. Formatted with a page number.

lastch_s
  ``Last Chapter ({page})``

  Chapter navigation button alt text. Formatted with a chapter number.

lasts_s
  ``Last``

  Showed below navigation arrow.

lastsch_s
  ``Last``

  Showed below navigation arrow on chapter-view pages.

  Separate from the regular page version because "page" and "chapter" have different grammatical genders in some languages.

meta_link_s
  ``Metadata ({file_ext})``

  Used on meta line. Formatted with the type for metadata.

meta_s
  ``Metadata``

  Heading on comic and chapter-view pages if there is no commentary.

next_s
  ``Next (#{page})``

  Alt text for page navigation. Formatted with a page number.

nextch_s
  ``Next Chapter ({page})``

  Chapter navigation button alt text. Formatted with a chapter number.

nexts_s
  ``Next``

  Showed below navigation arrow.

nextsch_s
  ``Next``

  Showed below navigation arrow on chapter-view pages.

  Separate from the regular page version because "page" and "chapter" have different grammatical genders in some languages.

no_comment
  ``The author has not provided commentary for this comic.``

  Used internally if there is no commentary.

no_transcript
  ``The author has not provided a transcript for this comic.``

  Used internally if there is no transcript.

notitle_chapter_s
  ``Chapter {chapter}``

  Equivalent of ``chapter_s`` without a title, for comics that only have chapter numbers.

page_alt_s
  ``Comic Page``

  Used as comic page alt text.

page_s
  ``Page``

  Base word for a comic page. Not currently used, but retained for future purposes.

permalink_s
  ``Permalink``

  Used on the meta line.

prev_s
  ``Previous (#{page})``

  Alt text for page navigation. Formatted with a page number.

prevch_s
  ``Previous Chapter ({page})``

  Chapter navigation button alt text. Formatted with a chapter number.

prevs_s
  ``Previous``

  Showed below navigation arrow.

prevsch_s
  ``Previous``

  Showed below navigation arrow on chapter-view pages.

  Separate from the regular page version because "page" and "chapter" have different grammatical genders in some languages.

range_separator
  ``–``

  Separator used for year ranges in copyright statements + multi-page numbers.

rss_s
  ``RSS Feed``

  Used for RSS icon alt text.

skip_s
  ``Skip to main content``

  Skip link text. Used on all pages.

source_s
  ``Source``

  Used on the meta line to indicate the original URL of a comic.

statline_s
  ``Posted by {author}, {date}``

  Used on the meta line.

statline_separator
  `` &mdash; ``

  Separator element used on the meta line.

store_s
  ``Store``

  Used in top navigation.

strf_format
  ``%Y{y}%m{m}%d{d}``

  Formatting string passed to strftime. Used on comic and chapter-view pages and in archives.

stylesheet_name_s
  ``Standard``

  The name of the stylesheet.

  Not visible to most users, honestly.

tag_s
  ``Tag``

  Used in page title for tag indices.

tags_s
  ``Tags``

  Used on the meta line and the archive heading.

toc_s
  ``Table of Contents``

  Used on archives.

transcript_link_s
  ``Transcript ({file_ext})``

  Used on the meta line. Formatted with the file type of transcripts.

transcript_s
  ``Transcript``

  Heading used on comic and chapter-view pages.

Language Coverage
-----------------

+-----------+--------------+-------------------------------------------------------------------------------------+
| Language  | Strings (#)  | Missing Translatable Strings                                                        |
+===========+==============+=====================================================================================+
| en        | 69           |                                                                                     |
+-----------+--------------+-------------------------------------------------------------------------------------+
| ja        | 67           | ccpdw                                                                               |
+-----------+--------------+-------------------------------------------------------------------------------------+
| de        | 66           | ccpdw                                                                               |
+-----------+--------------+-------------------------------------------------------------------------------------+
| es        | 62           | all_pages_s; ccpdw; jsonfeed_descr; toc_s                                           |
+-----------+--------------+-------------------------------------------------------------------------------------+
| fr        | 60           | about_s; all_pages_s; ccpdw; chapbook_page_alt_s; jsonfeed_descr; page_alt_s; toc_s |
+-----------+--------------+-------------------------------------------------------------------------------------+

Other languages' translations are not yet complete enough to appear in
this table.
