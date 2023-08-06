# Springheel Changelog

## 7.0.2

+ SHA-256 checksums are now calculated for all strips during the generation process, and are available through the site.json endpoints file.
+ The endpoints file also adds a list of "authors" for each category, and the Springheel version used to build the site. Its listing of chapter info is more useful as well.
+ "plain" theme now includes an experimental dark variant activated by [prefers-color-scheme: dark](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme).
+ The code has been cleaned up and refactored in several places, mostly to reduce repetition.
+ Springheel now automatically adds a trailing slash to the end of `base_url` if it is missing.
+ Files referenced on the Extras page are now copied asynchronously.
+ Fixed some errors when comics didn't have license URIs.
+ Fixed flow direction for chapter pages in right-to-left mode. This updates all themes and some templates.

## 7.0.1

+ Minor updates to documentation and file manifest.
+ Improved extra generation's file size calculator.

## 7.0.0 "Chilchuck"

It's Springheel's biggest release yet! I've changed or improved almost every aspect of the program, so there's almost too much to describe.

### New Features

+ Springheel now accepts metadata, transcript, and character files in JSON format. It expects the extensions ".meta.json" and ".transcript.json" for the former (respectively); character files can be named whatever you like, as they're specified in the comic configuration. Set `json_mode` in `conf.ini` to True to try it out. The tutorial has detailed syntax examples. Note that generation may behave erratically if some input files are JSON and others are not; if you're going to use JSON mode, make sure to convert all metadata, transcript, and character files to JSON format first.
+ A new command line script, `springheel-addimg`, will automatically generate metadata files for strip images.
+ Springheel now automatically detects sizes for all images, removing the need to manually specify them in metadata. Dimensions are also stated in the output HTML, so page elements do not move or jitter as images load. This feature and `springheel-addimg` add [Pillow](https://pypi.org/project/Pillow/) as a dependency.
+ You can now create "webtoon"-style comics with multiple image files per strip! Set `mode` to "webtoon" in both the comic `.conf` and the strip's metadata, then add a list of image filenames to the latter as `pieces:`, à la `pieces: panel2.png, panel3.png`.
+ Springheel now contains proper documentation built with Sphinx. It's the future! The rst files can be found in `docsource` when you download Springheel's source code, but they're mostly just automodule stuff, so I don't know how useful they'll be. I also built them with my own customized theme, so locally-produced output may vary. Note that you'll need the numpydoc extension to build the docs from source.
+ Springheel can now generate "about" pages with long descriptions of comics, optionally with a subset of HTML. To use it, set `about` to True in `conf.ini` and define the about section in the relevant `.conf` file with "`about = `". You can include line breaks by writing `\n` where needed. This feature adds a new dependency on [html-sanitizer](https://pypi.org/project/html-sanitizer).
+ Some non-integer page numbers --  decimals (like "6.5") and double-page ranges (like "116–117"; en dashes and hyphens both work) -- are now accepted.
+ Alt text on navigation arrows includes numbers, so assistive tech users can more quickly tell where they are actually going (without having to look at other areas of the page, identify relevant bits of long URLs, etc.).
+ Added a new "chapter view" -- if chapters are enabled, you can generate pages for each chapter that show all that chapter's strips (and the appropriate metadata) and allow navigation between chapters; as with individual comics, navigation will not appear if there is only one chapter. On sufficiently wide screens, two pages appear side by side, much like pages of a physical book.
+ The separator between stat line elements is now a translatable template string, so you can edit it locally if you want a different one.
+ Allow setting raw HTML copyright/license statements with `license_html` in .conf files.
+ The date formatting string is now editable in strings.json. Caveats: for compatibility, there is no single string passed directly to strftime. Instead, the values of `strf_format` (default: "%Y{y}%m{m}%d{d}") and `date_format` (list of 3 strings, can be "") are combined. Warning: because of the variety of different areas of the code where dates are used, substantial changes to `strf_format` may cause unpredictable problems during build.
+ The extras page now indicates the size of downloadable files in bytes, kibibytes, or mebibytes.
+ You can now manually specify slugs. For categories, add a line like `slug = desired-slug` to the `.conf` file. For strips, add `title_slug: desired-slug` to the `.meta` file. (Strip slugs are only used in image rename patterns.) This is especially useful for non-ASCII languages that get odd output from the existing slug system.
+ Added rudimentary support for OpenGraph and Twitter Card tags.
+ If a comic is based on an existing work, you can now add a link to the source in its `.meta` file à la `source: https://example.com`, and it will appear in the statline.
+ Springheel's command-line messages are now translatable with gettext, making the program easier to use in other languages.
+ Type hints have been added to all functions.

### New Default Themes

+ "elemental" subthemes "electricity", "ice", "wood", and "metal".
+ "staples"
+ "meikai"
+ "berryheart"
+ "blacktea"

### Improvements

+ File copying and similar features are now performed asynchronously, so they should be considerably faster. This increases the minimum Python version required to 3.7.
+ Previous/next buttons are no longer displayed if there is only one more strip in that direction (i.e., first/previous or next/last have the same value), to avoid having multiple buttons going to the same page.
+ If only one strip (or chapter) exists in a category, navigation is not generated at all.
+ Figure captions are no longer displayed if nothing has been set for them. (Of course actual alt text is present for the images themselves.)
+ "Permalink" has been added to the stat line.
+ Chapters no longer must have titles (this was intended to be the case already, but I forgot).
+ Transcript parsing is much neater and cleaner, and accepts more line endings.
+ *Lots* of fixes to make the code faster and cleaner.
+ Tuned up all themes and templates significantly. They are cleaner and more accessible all around.
+ The "twothousand" theme in particular has been almost entirely rewritten. It should be less ugly and more faithful to the era it evokes.
+ Category/chapter/page information has been moved to the stat line ("Posted by Jane Smith on such-and-such date"), and links to the chapter-view page if applicable.
+ Copyright footer information is more detailed, especially when strips in the same category have different authors.
+ Copyright years are now listed as a range from the original posting date to the current year as of site-generation time.
+ Meta lines include links to transcript files, instead of just metadata files.
+ Springheel now fails to build if a page without a chapter specified is in a category that *is* divided into chapters. (At present, Springheel is not designed to allow this.)
+ Post dates are now displayed in archives.
+ On Japanese sites, dates now appear formatted like "[year]年[month]月[day]日", as this isn't substantially different from ISO 8601.
+ Table of contents generation has been expanded to include non-chaptered comics.
+ The scrollto preference has been removed, as it was causing issues with other necessary features.
+ Comics without transcripts no longer display a message to that effect on generated pages. I reasoned that it was confusing to have a "transcript" heading if there was in fact no transcript present. The JSON endpoints file will still contain `transcript_c: "<p>The author has not provided a transcript for this comic.</p>"` (or the equivalent in the site language) for consistency.
+ In the same vein, comics without commentary do not display the "no commentary" message and have the "Commentary" heading switched out for "Metadata".
+ The links to metadata and transcript files now indicate the approximate type of file they are. In default mode, this will be "YAML" for metadata and "TXT" for transcripts, and in JSON mode, "JSON" for both.
+ Made it less annoying to add new fields to `strings.json`.
+ Logging has been improved and now defaults to off. To enable it, just add `--logging` as an argument to `springheel-build`.
+ Skip-navigation links are now always visible in all themes, rather than being visually hidden until activated.
+ The "home" link in top navigation has been removed, and the header image is now a link to the home page.

### Bugfixes

+ Finally switched the meanings of "header" and "banner" in configuration files and templates, and renamed the `banner_filename` option in `conf.ini` to `header_filename`. This is a backwards-incompatible change. (I originally got them the wrong way around by mistake, and was waiting for a major version to fix it.)
+ Navigation goes only to *existent* pages, to avoid 404 errors from numbering gaps.
+ If multiple comics on a multi-theme site use the same theme, that theme is no longer relentlessly duplicated by the stylesheet concatenation process.
+ Comics are now sorted consistently on index and archive pages.
+ Chapter titles no longer contain trailing newlines.
+ If a comic has multiple authors, this is reflected in the JSON Feed.
+ Characters are attributed to the correct comics in the site JSON endpoints file.
+ Commentaries no longer contain empty `<p>` elements.

No matter how many times the Sun rises or the Moon sets, like the lodestar above that guides us, may the winds of fortune ever blow your way.

## 6.0.3
+ Fixed a bug that kept headers and banners from copying to output under some circumstances.

## 6.0.2
+ Removing some accidental JSON debug output from building. ^_^;;

## 6.0.1
+ Replaced awesome-slugify with [python-slugify](https://pypi.org/project/python-slugify/), as the former is no longer actively developed.
+ Minor updates to JSON Feed generation to comply with version 1.1 of the spec.

## 6.0.0 "Ukyou"
+ Added new themes "fluff", "crystal", and "elemental" (which is configurable, like "seasonal").
+ Added progress bars for time-consuming parts of site generation, like finding images and creating tag index pages. This feature adds [tdqm](https://pypi.org/project/tqdm/) as a dependency.
+ Added rudimentary [JSON Feed](https://jsonfeed.org/) support. I hacked this together myself based on existing JSON endpoint bits; it validates, but should be considered experimental.
+ Added feature to generate tables of contents on archive pages if the comic has chapters.
+ Improvements to the "book", "fairy", "gothic", and "city" themes.
+ Optimized some graphics slightly. There should be little or no visual difference.
+ Cut some unneeded mixin imports from the theme SCSS files.
+ Fixed an error in the default conf.ini -- `scrollto` was mistakenly listed as `skipto` and so did not work.
+ Fixed several bugs in non-chaptered comic archives.
+ Changed the recommended alternate value of `scrollto` from "comic" to "topbox" so that above-strip navigation can still be accessed. "comic" is still accepted as a valid value for `scrollto`.
+ Added `scrollto` to archive links as well.
+ Allow disabling `scrollto` by setting it to `False`.
+ Added classes and I.D.s to some elements that did not have them.
+ Added social button for Mastodon.
+ RSS feed generation bugfixes: less hacky output selection and comment creation, and strips with a more recent date will appear closer to the top of the XML file.
+ Cleaned up social media icon code and markup a bit.
+ Removed trailing spaces that were accidentally inserted after speaker identifiers in transcripts.
+ Many improvements to the HOWTO.md tutorial file.
+ Adding page URL as an argument to `format()` when generating pages. If you want to add something like a "share" button to your page templates (per the "Extending Springheel Sites" section of HOWTO.md), you can use `{url}` in place of a static permalink. Springheel will now replace that with the page's URL.
+ The default alt text that appears when `alt` is unset is now more informative.
+ Page numbering now sensibly allows for page number 0. (It previously started from 1.) This allows for cover pages and the like without creating confusing constructions like "Page #2 'Page 1'".
+ If they exist, some non-strip assets (e.g. stylesheets, site graphics, navigation arrows) are no longer rewritten when building, to avoid them being copied and re-copied over and over. Delete `output/assets` and `output/arrows` if you do want to overwrite these files.

## 5.2.4
+ Alt text for comic pages is now a translated string.
+ Extra images now have alt text, allowing screen readers on some platforms to announce their captions properly.

## 5.2.3
+ Finally accepted that my paltry attempt to support favicons was in error. Users who want to add favicons should edit their site's local templates (the old/bad favicon code has been replaced with a comment indicating where to insert the output from a dedicated favicon generator) and manually copy the appropriate files into `output`.
+ Fixed a couple of minor HTML errors in templates (mostly extra whitespace and single-quoted elements) and the processing of same.

## 5.2.2
+ Improved metadata parsing a bit.
+ Added missing docstrings.
+ Fixed some quirks in page-footer copyright statements.
+ Cleaned up some unused functions.
+ Updated HOWTO.md

## 5.2.1
+ Removed the `langcodes` dependency. Multi-language site linking should work the same as before, if not better.
+ Added display of the original language code as a fallback if Springheel doesn't know the proper name for a language during multi-language site linking.

## 5.2.0 "Bossun"
+ Made it possible to insert links to your Springheel site in other languages in the site footer, using the new `multilang` config option. Notably, this adds `langcodes` as a dependency (to display the language names correctly).
+ Added functionality to generate a JSON file (`output/site.json`) with detailed information about the site, including URL endpoints. This should theoretically make it easier to extend Springheel sites with other programs.
+ Fixed an error in social icon spacing. (Re-init any existing site templates.)
+ Updated HOWTO.md

## 5.1.0 "Senku"
+ Added a configuration option for skip links and comic navigation to scroll directly to the comic image, instead of to the page title.
+ Fixed an error that was preventing sites' local `strings.json` files from being used.
+ Completely rewrote comic navigation.
+ Started work on a Spanish translation. It's incomplete and likely weird in many places; I don't actually speak Spanish. (The translation is based entirely on poking around on Spanish webcomic sites to see how they render the common terms, double-checking with several dictionaries.)
+ Started a French translation in the same way, although I'm even less sure of this one's accuracy.
+ Removed references to GitHub from `setup.py` and templates in protest of their contract with ICE.

## 5.0.3
+ Fixed a major bug where comics on multi-comic sites were added to the wrong chapters.
+ Corrected the error message that appears if "status" is unset.

## 5.0.2
+ Fixed a bug where tag page results weren't being sorted correctly.
+ Archive page titles for single-comic sites are now translatable.
+ Fixed an error where colons couldn't be used in some metadata fields.
+ Removed the long-unnecessary language prompt when running `springheel-init`.
+ Lots of improvements to all themes. (Make sure to re-run `springheel-init` to update your stylesheets)

## 5.0.1
+ Started escaping most things that will appear as HTML.

## 5.0.0 "Azumane"
+ Added proper tagging system.
+ Added option for zero-padding page numbers.
+ Cleared out some unused stuff from archive and navigation generation + the default conf.ini
+ Fixed some issues with image renaming.
+ Fixed error where chaptered works sometimes appeared twice on archive pages.
+ Started naming major/minor versions ~~after hot anime dudes~~

## 4.1.0
+ Springheel now generates XML site maps of comic sites.
+ Cleaned up logging a bit.

## 4.0.0
+ Added new themes "revolution", "fairy", "sysadmin", and "might".
+ Separated traits from descriptions on character pages.
+ Fixed major error where a multi-comic site wouldn't generate if some comics had a characters file and some didn't.
+ Fixed bug where slugs were not URL-safe.
+ Fixed bug where the archive page's main heading wasn't getting translated.
+ Fixed bug where extras pages used a comic's title and banner, instead of the sitewide ones.
+ Slight improvements to "seasonal" and "showtime" themes.

## 3.0.3
+ Fixed a very stupid copy+paste error that caused public domain comics to be described as published from a U.R.L. (instead of their respective country).

## 3.0.2
+ Did a better job fixing the character bug from the previous version.
+ Fixed an error where non-transcribed comics wouldn't generate on Windows.
+ Fiddled with the markdown in HOWTO.md because it was displaying strangely in some programs.

## 3.0.1
+ Fixed a bug where archives weren't generating correctly for non-chaptered comics.
+ Fixed a bug where the ordering of character attributes changed randomly every time the page was regenerated.
+ Updated some information in the default conf.ini file.

## 3.0.0
+ Added extras page functionality
+ Added new theme "showtime"
+ Corrected <title> elements for character pages
+ Improved logging

## 2.0.0
+ Condensed template files into one
+ Improved accessibility
+ Updated translations

## 1.0.2
+ Fixed a bug where archives couldn't be generated for multi-comic sites.

## 1.0.1
+ Fixed the parts of the readme that said arrow was a dependency (it isn't).
+ Fixed a bug where .sass-cache was getting installed as if it were a theme.

## 1.0.0

+ Streamlined config files.
+ Tidied up all stylesheets and templates.
+ Added some more translation strings.
+ Refactored a whole lot of code and made it neater.
+ Fixed miscellaneous bugs.
+ Added new themes "rock" and "western".
+ Added better arrows for some themes.
