How to use Springheel
=====================

This is a walkthrough for getting Springheel working, setting up a comic
site, and updating it. (Using an FTP program, registering a domain name,
creating an SSH key, etc. are outside the scope of this guide.)

Get Springheel
--------------

Springheel requires at least **Python 3.7.** Versions before Springheel
7.0 require Python 3.5. No version will work with Python 2.

To install from PyPI, simply run

::

   $ pip install springheel

To install from source, you’ll need the following dependencies:

-  `Feedgenerator <https://pypi.org/project/feedgen>`__
-  `python-slugify <https://pypi.org/project/python-slugify>`__
-  `tdqm <https://pypi.org/project/tqdm>`__
-  `html-sanitizer <https://pypi.org/project/html-sanitizer>`__
-  `Pillow <https://pypi.org/project/Pillow/>`__

A pre-built version of the documentation is available in the source
package. Thus, the following dependencies are optional, but are needed
to build documentation from source:

-  `Sphinx <https://pypi.org/project/sphinx>`__
-  `Numpydoc <https://pypi.org/project/numpydoc>`__

To build documentation in the HTML format, you will also need a Sphinx
theme called "pyramida"---you can either edit the value of
``html_theme`` in ``docsource/conf.py``, or open your Sphinx theme
directory and create a symbolic link from the existing "pyramid" theme
to "pyramida".

Navigate to the springheel directory, start up your virtual environment
if you're using one, and run ``setup.py install``. (You may need to run
this with ``su -c`` or ``--user`` depending on the type of Python
install you have).

**Important**: If you’re on Windows and get an error about Visual C++
while installing dependencies (lxml especially), do not panic! Just use
PyPi to install that specific library directly, then try to install
springheel again.

After updating Springheel to a new version, you should generally
re-initialize any existing comic sites in case there were changes to the
themes or template files. For major versions in particular, check
``conf.ini`` against the default one in your install directory (it’s
easier with a graphical merge tool like
`Meld <http://meldmerge.org/>`__) and add any new configuration options.
(``springheel-init`` doesn’t alter or replace configuration files.)

Limitations
-----------

Springheel is designed to be as simple and bare-bones as possible, so
there are some features it doesn’t have (or just doesn’t have *yet*).
E.g.:

-  The RSS feed may list items out of order if multiple comics have the
   same posting date.
-  Page commentaries and character descriptions are plain text only (no
   HTML). This is because parsing markup in those blocks would be *much*
   more complicated and slow.
-  Templates have not been translated into many languages yet, and the
   ones for languages I don’t personally speak may be inaccurate.
-  It’s not possible to have a single site with multiple languages; you
   can only generate separate sites for each language and display links
   to the other sites.
-  There is no out-of-the-box support for ads or analytics. See
   “Extending Springheel Sites” below.
-  Feeds are sitewide (as opposed to one for each individual series out
   of many) and bare-bones. RSS feeds don’t display thumbnails of the
   comic, the strip itself, or anything along those lines. (But this may
   actually be your desired behavior for RSS feeds, in which case,
   super!)
-  Pages do not use any kind of modernizer or polyfill, so they will not
   look *exactly* the same in older browsers that they do in
   bleeding-edge new ones. They’ll still be perfectly usable, just a bit
   less fancy. Remember, `it doesn’t have to look the
   same <http://www.edgeofmyseat.com/blog/2002-04-01-it-doesnt-have-to-look-the-same>`__.
-  There is no support for responsive image loading with ``srcset`` or similar yet.

Building a site for Wuffle
--------------------------

I’ve provided a sort of “sample site” pack based on a few strips from
*Wuffle*, a cute comic which is public domain. `Download it
here <https://twinkle-night.net/Downloads/springheel-wuffle-sample-site-pack.zip>`__
and let’s walk through the process of using it, step-by-step.

Initialization
~~~~~~~~~~~~~~

To start off, make a directory for this project, and navigate there in
your terminal of choice. (You should probably put the ZIP file here to
make sure you don’t lose it.)

Next, we’ll run the initialization script. On GNU/Linux this is simply
``springheel-init``.

On Windows, add Python's Scripts directory to your system path (if you
haven’t already), restart as needed, and run ``springheel-init.exe``.

If all goes well, some debug info will appear explaining what is going
on: the script locates where Springheel was installed, grabs the
templates and other base assets, and copies them to your current
directory.

Now unzip the contents of the *Wuffle* pack,
``springheel-wuffle-sample-site-pack.zip``, into the current directory.
Everything in it *except* the ``wuffle_conf.ini`` file should go into
``input``. Remove the current ``conf.ini`` file and rename
``wuffle_conf.ini`` to simply ``conf.ini``.

Your directory should now look something like this:

.. code-block:: text

   .
   ..
   arrows/
   input/
   socialbuttons/
   templates/
   themes/
   conf.ini

Let’s look at each of these in more detail. You can also skip right down
to “Trying to build” and work out this stuff once you already have a
generated site to compare it to; the choice is yours.

Base directory
^^^^^^^^^^^^^^

This holds the sitewide configuration file and the input and output
folders.

``conf.ini`` is a sitewide configuration file. You’ll definitely want to
modify it before building, as we’ve done here – some of the defaults are
deliberately silly or non-working.

Asset folders
^^^^^^^^^^^^^

``arrows`` holds the navigation buttons – they follow the scheme
{theme}_{direction}. You can easily make your own if you don’t like the
defaults.

Social buttons are 24x24 icons that are used to link to social media
sites, like Twitter or Pump. These are also simple to customize. Adding
a site that isn’t supported is a bit more involved but still entirely
possible.

Input
^^^^^

As per the name, this holds the comic files (images and metadata). Site
banners and such go here as well. Right now, this should contain:

-  10 comic images
-  10 .meta files
-  10 .transcript files
-  1 .conf file
-  1 .chars file
-  2 heading/banner images

Templates
^^^^^^^^^

These are the templates used to generate the finished pages. One is a
JSON file that contains all the translations, and the rest are HTML
files.

As long as they’re not based on machine translations, improvements to
any language and pull requests for languages I haven’t provided are
welcome!

Themes
^^^^^^

Themes determine the look and feel of your site. I’ve tried to include a
big variety of default themes, while also keeping each theme

-  **small**: even counting graphic assets, the median theme filesize is 16
   KiB; the very largest theme is still under 100 KiB.
-  **simple** enough to make your own themes that hook into the existing
   code easily: no nested wrappers or complex positioning. They're based on
   semantic HTML that should be easy to alter however you wish.
-  and **accessible**, because everyone reads comics. They have big text, use
   color schemes that pass WCAG AAA-level standards for text contrast (no thin
   cyan text on a white background here), highlight active and focused links
   very obviously, and include easily-visible "skip navigation" links, and
   should look fine on most small screens.

All themes share a generic "print" stylesheet, which makes the experience of printing a comic page a bit more pleasant.

Our *Wuffle* example uses the ``plain`` theme for simplicity, but it’s
by no means the only option. See `Themes <themes.html>`__ for more info.

Rolling your own
''''''''''''''''

Creating your own styles is simple enough. Here’s what you must do:

1. Go to the ``themes`` directory, and make a folder there with the
   title of your theme. It must be a unique name, all lowercase, and
   without spaces.
2. Create a file there called ``style.css``. How you create
   ``style.css`` does not matter, as long as it is called that and in
   the right place. For neatness and ease of memory, I usually use Sass
   to make a .scss file in ``themes``, and have it compile to a
   ``style.css`` in a matching directory
   (e.g. themes/plain.scss:themes/plain/style.css). If you’re using any,
   put all other assets, like images, in the same directory as
   ``style.css`` too.
3. Design your cool CSS theme. This is the easy part. :)
4. Make a set of navigation arrows and put them in ``arrows``. For
   compatibility with Springheel’s code, they should be like this (even
   if you want the arrows to point the other way, just follow this
   schema, open up ``conf.ini``, and set ``navdirection`` to ``rtl``):

-  {yourtheme}_first.png (pointing **left**)
-  {yourtheme}_prev.png (pointing **left**)
-  {yourtheme}_next.png (pointing **right**)
-  {yourtheme}_last.png (pointing **right**)

5. **Test out your theme.** Run your colors through `WebAIM’s Color
   Contrast Checker <http://webaim.org/resources/contrastchecker/>`__.
   See what it looks like when zoomed in or out really far. If you can,
   check what it looks like on different browsers and devices, or with
   automatic image-loading turned off. Ask friends for help if you need
   to. Try to validate your stylesheet; it doesn’t necessarily have to
   follow W3’s official specification, but there ought to be a good
   reason why it doesn’t.
6. No, really, actually do #5. Your readers will thank you.
7. Set ``site_style`` to the theme name you decided on in step 1 and run
   Springheel to regenerate your comic. Your comic site will now be
   themed with your own, custom theme!

One thing to keep in mind that you may have noticed already: each
theme’s CSS is wrapped in an ID selector, and pages that use a given
theme set the ID of ``html`` to that theme’s name. (So, a page that uses
the “plain” style will have “``<html lang="[whatever]" id="plain">``”,
and plain’s ``style.css`` only applies to elements within ``#plain``.)
If you don’t do the same, and your site uses multiple themes, it won’t
display correctly at all and will look very weird.

Setting comic metadata
^^^^^^^^^^^^^^^^^^^^^^

The comic images and their metadata will end up in ``input``. Springheel
decides a file is a comic page if it has 1. a matching metadata file and
2. one of the following extensions (case insensitive):

-  .png
-  .gif
-  .jpg or .jpeg
-  .svg
-  .webp (not recommended as many browsers do not support it yet, but
   use your own judgement)

The metadata file has the same name as the comic image, just with the
extension ``.meta``. If the comic has a transcript file (strongly
encouraged), that will similarly have the extension ``.transcript``.

(In JSON mode, the extensions are ``.meta.json`` and ``.transcript.json``,
respectively.)

Comic series as a whole (rather than individual strips) also have
metadata files. The main one required is a configuration file that ends
with ``.conf``. You can optionally declare a ``.chars`` file that will
generate a series character page. And if your comic is divided into
chapters, you can also add a ``.chapters`` file that maps chapter
numbers to chapter titles. We’ll discuss these more shortly.

The strip ``.meta`` file will have various key metadata about the comic
(and the author’s commentary, if applicable), while the ``.transcript``
is, as the name suggests, a textual transcript of the comic’s action and
dialogue. The .conf file contains important preferences about the
series. The syntax for these files is fairly straightforward.

For this example, let’s use a specific `Wuffle
comic <http://www.wufflecomics.com/2012/03/wuffle-and-aunty-pinky-2/>`__
– look for ``Wuffle_2012-03-21-2012_0004_Aunty.jpg`` and its related
files in the ``input`` directory.

Here’s what ``Wuffle_2012-03-21-2012_0004_Aunty.meta`` looks like:

.. code-block:: yaml

   ---
     title: Wuffle and Aunty Pinky
     author: Piti Yindee
     email: <expunged>
     date: 2012-03-21
     tags: 4 panel series 1, Aunty Pinky, Wuffle
     conf: Wuffle.conf
     category: Wuffle
     page: 4
     height: 1429
     width: 1000
     language: en
     mode: default
     chapter: 1
     alt: This is a test of the extra text system.
   ---
   Meet the new Wuffle's neighbor, Aunty Pinky aka the money hunger!

Here’s the transcript file,
``Wuffle_2012-03-21-2012_0004_Aunty.transcript``:

.. code-block:: text

   (Wuffle paints a fence as Aunty Pinky looks on.)

   Wuffle
     It's done, ma'am.

   Pinky
     Thanks, sweetie.

   (Pinky offers Wuffle a wad of money. He looks sheepish.)

   Wuffle
     Oh, it's fine, ma'am. Please keep your money.

   Pinky
     Oh, well. More for me.

   (Pinky begins eating the money.)

And finally ``Wuffle.conf``, the configuration file for the *Wuffle*
series in general:

.. code-block:: yaml

   [ComicConfig]

   category = Wuffle
   author = Piti Yindee
   email = <expunged>
   header = WuffleHeader.jpg
   banner = WuffleHeader.jpg
   language = en
   mode = default
   status = complete
   chapters = Wuffle.chapters
   desc = Public domain funny animal comic
   chars = Wuffle.chars
   license = To the extent possible under law, Piti Yindee has waived all copyright and related or neighboring rights to Wuffle Comic.
   license_uri = http://creativecommons.org/publicdomain/zero/1.0/

In ``.meta`` files, the metadata is sandwiched between the ``---``
lines; below that is the author’s commentary. The strictly needed fields
are:

-  **title** (the title of this specific strip or page)
-  **author** (you! or rather, whoever is supposed to get the credit for
   posting a page)
-  **email** (your email address – this is needed for RSS feed
   generation)
-  **date** (the strip’s publication date, in ISO 8601 (YYYY-MM-dd)
   format)
-  **category** (the comic/series title)
-  **page** (this strip’s page number)
-  **language** (ISO 639-1 code)

You can also add a ``chapter`` number if this strip is part of a
chapter; ``alt_text`` for an extra line or two that will appear below the
comic; and/or ``source`` (version 7+) if the comic is based on an
existing work and you want to link to the original.

The .transcript has the character names, their dialogue indented by 2
spaces, and actions offset by parentheses. As long as it follows this
scheme, it’ll be parsed by the HTML transcript generator.

The .conf file has fields that are required for accurate copyright
statements, RSS feed generation, and general series organization:

-  **category** (the name of the series)
-  **author** (again: you!)
-  **email** (your email address)
-  **header** (a header image that will appear at the top of this
   series’ pages)
-  **banner** (a banner to identify this series; can be the same as the
   header or different)
-  **language** (ISO 639-1 code)
-  **chapters** (whether or not the comic is divided into chapters. If
   you set this to True *or* the name of a ``.chapters`` file, the
   archives page will automatically be separated by chapter)
-  **desc** (a description of the comic; used for the index page and RSS
   feeds)
-  **status** (whether the series is finished or not; accepted values
   are ``in-progress``, ``complete``, and ``hiatus``)
-  **chars** (optional; the filename of a .chars file. If
   characters_page in ``conf.ini`` is set to True, this will generate a
   characters page based on the linked file.)
-  **about** (optional; if about pages are enabled in conf.ini, a string
   or HTML snippet that describes this comic.)

Automating the addition of new strips
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(New in version 7)

You can use the ``springheel-addimg`` script to automatically generate
metadata files for images in input.

You can provide information like title and page number when prompted,
or you can do so as command line arguments:

-i INPUT, --input INPUT
  The strip's image filename.

-c CONF, --conf CONF
  The category .conf file to use.

-t TITLE, --title TITLE
  The strip's title.

-n NUM, --num NUM
  The strip's page number.

-k CHAPTER, --chapter CHAPTER
  The strip's chapter number.

-a ALT, --alt ALT
  Extra text for the strip.

-s SOURCE, --source SOURCE
  The strip's source URL.

-j, --json
  Output metadata as a .meta.json file (for JSON mode).

--commentary COMMENTARY
  Commentary on the strip.

For example:

.. code-block:: bash

   $ springheel-addimg -i input/test.jpg -c input/Wuffle.conf -t "Test" -n 11 -k 1 -a "Test extra text" -j --commentary "Test commentary"

...might generate the following test.meta.json:

.. code-block:: json

    {
       "metadata": {
           "title": "Test",
           "author": "Piti Yindee",
           "email": "notreallyyindeesemail@notareal.tld",
           "date": "2021-03-23",
           "conf": "Wuffle.conf",
           "category": "Wuffle",
           "page": "11",
           "height": 1429,
           "width": 1000,
           "language": "en",
           "mode": "default",
           "commentary": ["Test commentary"],
           "chapter": "1",
           "alt": "Test extra text"
        }
    }

Other notes:

-  addimg checks for date-like patterns in the filename, and if it
   can't find any, defaults to the last-modified time reported by
   Python's ``os.stat()``.
-  It can't yet add tags or pieces (see below); you'll have to edit
   those in manually.

Webtoon Mode
^^^^^^^^^^^^

(New in version 7)

If you want to make long-strip comics in the style of South Korean
“`webtoons <https://en.wikipedia.org/wiki/Webtoon>`__”, where comic pages
are made of multiple image files, you can enable webtoon mode.

Create a ``.meta`` file for the first image. In both the category's
``.conf`` file and the ``.meta`` file, set ``mode`` to ``webtoon``.

Then add a ``pieces`` field to the metadata file that lists all the
page image files in order, starting from the second one.

It will look something like this:

.. code-block:: yaml

      mode: webtoon
      pieces: longstrip001_002.jpg, longstrip001_003.jpg

In JSON mode, ``pieces`` will be a list, just like tags:

.. code-block:: json

    "mode": "webtoon",
    "pieces": ["longstrip001_002.jpg", "longstrip001_003.jpg"],

This is all that's needed; Springheel will automatically copy and rename
the images listed as pieces, and they'll appear on both comic and
chapter pages.

Chapter view will not display pages from webtoon chapters side-by-side,
no matter how wide the screen is.


Character pages
^^^^^^^^^^^^^^^

Webcomics are notorious for having out-of-date character pages, so I
made them as easy as possible for Springheel. Here’s all you have to do:

1. Make a file to hold your character markup in ``input``. I’d recommend
   calling it with the name of the series and the file extension
   ``.chars`` to make it easy to remember. Let’s use Wuffle.chars for
   this example.

2. Add the category and language to the top of the characters file,
   followed by a line with “``---``”.

   .. code-block:: yaml

       category: Wuffle
       lang: en
       ---

3. Add characters! The syntax is very simple. Mark character names with
   ``name:`` and a short description or blurb with ``desc:``. You can
   optionally add a picture of the character with
   ``img: image_filename.ext``. (If you don’t want an image, use
   ``img: None`` instead.) Add a line with just ``---`` after each
   character to separate them.

4. The default attributes – name and description, and optionally an
   image – will be fine for a basic characters page. But you can add any
   other, custom text attributes you want, and they’ll be displayed too!
   All you have to do is type the attribute label you want, followed by
   a colon, and then the value (one attribute per line). Let’s suppose I
   want to include a “species” field because the *Wuffle* characters are
   anthropomorphized animals. For Wuffle himself, I’d add
   ``Species: Wolf``. Simple! All custom attributes are put into their
   own little subsection in the compiled page.

5. Add a line to the comic’s configuration file (Wuffle.conf in this
   case) pointing to the character file:

   .. code-block:: yaml

       chars = Wuffle.chars

6. Run Springheel as normal. You’re done! The character page will now be
   generated.

So this character file:

.. code-block:: yaml

   category: Wuffle
   lang: en
   ---
   name: Wuffle
   desc: Wuffle is a wolf with a big heart. Currently he's living as a farmer in a barn that is on a hill near Gingerbread Village. He never turns away from people who need a helping hand. He is also willing to help them out without expecting anything in return. However, Wuffle tends to be naïve and too trusting, which often brings him unexpected trouble.
   img: char-wuffle.jpg
   Gender: Male
   Species: Wolf
   ---
   ...

Would generate a character page like this:

.. code-block:: html

   <div class="char">
       <h2>Wuffle</h2>
       <img src="char-wuffle.jpg" alt="" />
       <dl>
           <dt>Gender</dt>
           <dd>Male</dd>
           <dt>Species</dt>
           <dd>Wolf</dd>
       </dl>
       <p>Wuffle is a wolf with a big heart. Currently he's living as a farmer in a barn that is on a hill near Gingerbread Village. He never turns away from people who need a helping hand. He is also willing to help them out without expecting anything in return. However, Wuffle tends to be naïve and too trusting, which often brings him unexpected trouble.</p>
   </div>
   ...

Which looks like this in the Plain style:

.. figure:: character-example.png
   :alt: Character example

   A simple character profile for Wuffle.

Of course, if you don't want a character page, simply set ``chars`` in your
comic's ``.conf`` file to "False".

Chapter titles
^^^^^^^^^^^^^^

If you want your work to be divided into chapters, you'll need a ``.chapters``
file. As described above, add a ``chapters: Wuffle.chapters`` line to
``Wuffle.conf``, then create a file called ``Wuffle.chapters``. In theory, all
you need to put in that file is a list of chapter numbers (one on each line),
but you can also add titles to the chapters.

Suppose we want the first chapter to be called “4-Panel Series 1”. We’ll
add the following line to ``Wuffle.chapters``:

.. code-block:: yaml

   1 = 4-Panel Series 1

That’s it! That title will appear on the archive page, as well as in the
headings for all pages that are marked as being part of chapter 1.

Note that series’ chapter settings are currently an either/or thing: you
can’t have some pages that are part of a chapter and some that are not.
If you have ones that don’t fit anywhere, I would recommend putting them
all into a “miscellaneous” chapter, or even converting to a multi-series
site and treating them as a separate (non-chaptered) series.

Extras
^^^^^^

Springheel allows you to create a page to hold various extras. The main
use case I was imagining was for guest art, wallpapers, textual
side-stories, etc., but you can really put anything you want there.

To create an extras page, pop open ``conf.ini`` and set ``extras_page``
to ``True``. Then put a JSON file called ``Extra.json`` in ``input``.
Here’s an example extras file for my sister’s comic, *Brutus*:

.. code-block:: json

   {
       "Fanart": [{
               "title": "Alucanth",
               "desc": "The very first Brutus fanart was a wonderful Alucanth by garrick!",
               "type": "image",
               "files": ["garrick_fanart_01.png"]
           },
           {
               "title": "Brutus MS Paint Poster",
               "desc": "Also by garrick: a big poster!",
               "type": "image",
               "files": ["garrick_fanart_02.png"]
           },
           {
               "title": "Just As Brutus'd",
               "desc": "Bardum contributes an amusing parody...",
               "type": "image",
               "files": ["bardum_fanart_01.png"]
           }
       ],
       "Comic": [{
           "title": "Brutus Comic Book Archive",
           "desc": "CBZ files for offline viewing. Read them with most any modern document viewer.",
           "type": "file",
           "files": [{
               "path": "Brutus_-_1-8.cbz",
               "link": "Brutus Chapters 1–8"
           }, {
               "path": "Brutus_Gaiden.cbz",
               "link": "Brutus Gaiden [incomplete]"
           }]
       }]
   }

That will generate an extras page with Comic and Fanart as the
second-order headings. ``file``-type items will appear as textual links,
and ``image``-type ones will appear as image elements with figcaptions.

Springheel adds file size indicators to links for ``file``-type downloads
automatically:

.. code-block:: html

    <h2>Comic</h2>
    <h3>Brutus Comic Book Archive</h3>
    <p>CBZ files for offline viewing. Read them with most any modern document viewer.</p>
    <ul>
        <li><a href="Brutus_-_1-8.cbz">Brutus Chapters 1–8 [2.2 MiB]</a></li>
        <li><a href="Brutus_Gaiden.cbz">Brutus Gaiden [incomplete] [132.7 KiB]</a></li>
    </ul>

Licensing
^^^^^^^^^

You are by no means required to relinquish the copyright of a comic
simply because you built the site for it with Springheel. The licensing
of your work is *entirely* your decision.

That being said, I want to promote `Free Cultural
Works <https://freedomdefined.org/Licenses>`__ in general, so Springheel
comes with some tools to make it easier to indicate the rights that
readers have.

First off, there is a field, ``license``, in ``conf.ini``. By default it
is “All rights reserved”. But if you want to release your comic into the
public domain, as Piti Yindee did for *Wuffle*, you could do something
like this:

.. code-block:: yaml

   license = To the extent possible under law, Piti Yindee has waived all copyright and related or neighboring rights to Wuffle Comic.

Note: if you are releasing your comic into the public domain, *please*
make sure to edit ``country`` in ``conf.ini`` to list the country you
are publishing from! This is very important because different countries
have different laws about the ability of authors to waive copyright.

If you’d rather use a Creative Commons license, you could add the HTML
snippet from their `license
chooser <https://creativecommons.org/choose/>`__, as I do on my own
site:

.. code-block:: yaml

   license = <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a> These <span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/StillImage" rel="dct:type">works</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Garrick</span> are licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

We add info on the license to the comic’s ``.conf`` file as well. For
public domain works this will be the waiver from before, as well as a
U.R.I. In *Wuffle*\ ’s case this might be:

.. code-block:: yaml

   license = To the extent possible under law, Piti Yindee has waived all copyright and related or neighboring rights to Wuffle Comic.
   license_uri = http://creativecommons.org/publicdomain/zero/1.0/

For a Creative Commons license, it will be the license’s name and
U.R.L.:

.. code-block:: yaml

   license = Creative Commons Attribution-ShareAlike 4.0
   license_uri = http://creativecommons.org/licenses/by-sa/4.0/

Now your comic will be nicely marked up with human- and machine-readable
license info!

Zero-padding
^^^^^^^^^^^^

(new in version 5)

By default, Springheel pads page numbers in URLs with zeros:
“page_0001”. Notably (to avoid breaking existing links), this isn’t
automatically updated if the total number of pages goes above 1000. If
you’re planning ahead and think you’ll need more digits, or (conversely)
if four digits is too much, just edit the ``zero_padding`` option in
``conf.ini``. If you want to turn off zero-padding entirely, simply set
it to ``False``.

Linking multi-language sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(new in version 5.2)

Let’s say you have a comic in both English and French, and you want to
handle both with Springheel. You generate a site for the English comics
and the French ones…but how will French-speakers who go to the English
site know that the French one even exists? With ``multilang``, you can
put a link to each site’s other language variations.

Open up your ``conf.ini`` and uncomment the line beginning with
``multilang``. It should then look like this:

.. code-block:: yaml

   multilang = xx=http://sample-springheel-comic.notarealtld/alanguage,xb=http://sample-springheel-comic.notarealtld/anotherlanguage

(If your conf.ini doesn’t have this option, no problem. Either update
your configuration based on the one that comes with the latest
Springheel version, or just add this line.)

Let’s say that we’re working on the English site’s ``conf.ini``, and we
want to add the French version, which is located at the URL
``https://fr.sample-springheel-comic.notarealtld``. We’ll modify the
line to:

.. code-block:: yaml

   multilang = fr=https://fr.sample-springheel-comic.notarealtld

And in the French site, we’ll add a link to the English one in the same
way:

.. code-block:: yaml

   multilang = en=https://en.sample-springheel-comic.notarealtld

Visitors to the English site will then see a link labeled “français” in
the footer, which goes to the French site – and the French site will
have an “English” one which goes to, well, the English one. Simple!

As in the default value, we can add links to multiple languages as well.
Just separate them with a comma (no spaces). For example, if we made a
German site too:

.. code-block:: yaml

   multilang = en=https://en.sample-springheel-comic.notarealtld,de=https://de.sample-springheel-comic.notarealtld

Springheel pulls the appropriate language autonyms from the project’s
``strings.json``. If your desired language isn’t in the default list,
you can either add it to that file *or*, in the multilang string, simply
use the language’s **name** instead of a two-letter code.

JSON Input
^^^^^^^^^^

(new in version 7.0)

By default, Springheel expects metadata, transcript, and character files
to use a YAML-like syntax. However, there is a setting in ``conf.ini``
called ``json_mode``. If you set this value to ``True``, instead of
reading ``.meta`` and ``.transcript`` files, Springheel will look for
``.meta.json`` and ``.transcript.json`` files, and it will default to
parsing character files as JSON as well. The output of JSON-based input
files is exactly the same as with the regular format.

Here are some example files to show the syntax.

Example meta.json
'''''''''''''''''

.. code-block:: json

   {
       "metadata": {
           "title": "Wuffle and Aunty Pinky",
           "author": "Piti Yindee",
           "email": "notarealemail@notareal.tld",
           "date": "2012-03-21",
           "tags": ["4 panel series 1", "Aunty Pinky", "Wuffle"],
           "conf": "Wuffle.conf",
           "category": "Wuffle",
           "page": "4",
           "height": "1429",
           "width": "1000",
           "language": "en",
           "mode": "default",
           "chapter": "1",
           "commentary": ["Meet the new Wuffle’s neighbor, Aunty Pinky aka the money hunger!"]
       }
   }

The main element is called “``metadata``”. Items that can have multiple
elements, even if they do only have one in a given file (like the
commentary in this case), are enclosed in brackets. (If there is more
than one item in a list, they are separated by commas.) Everything that
isn’t a list, including boolean values like “False”, should have
quotation marks.

Example transcript.json
'''''''''''''''''''''''

.. code-block:: json

   {
       "transcript": [{
           "line": "Wuffle paints a fence as Aunty Pinky looks on."
       },

       {
           "speaker": "Wuffle",
           "line": "It's done, ma'am."
       },

       {
           "speaker": "Pinky",
           "line": "Thanks, sweetie."
       },

       {
           "line": "Pinky offers Wuffle a wad of money. He looks sheepish."
       },

       {
           "speaker": "Wuffle",
           "line": "Oh, it's fine, ma'am. Please keep your money."
       },

       {
           "speaker": "Pinky",
           "line": "Oh, well. More for me."
       },

       {
           "line": "Pinky begins eating the money."
       }
       ]
   }

The root element is “``transcript``”. Lines are dictionaries. Speakers
are identified with “``speaker``”, and dialogue with “``line``”. If a
line doesn’t have a speaker, it’s parsed as an action/description line.
You don’t need to wrap it in parentheses (Springheel will do this
automatically when building).

Example JSON character file
'''''''''''''''''''''''''''

.. code-block:: json

   [
       {
           "name": "Wuffle",
           "img": "char-wuffle.jpg",
           "desc": "Wuffle is a wolf with a big heart. Currently he's living as a farmer in a barn that is on a hill near Gingerbread Village. He never turns away from people who need a helping hand. He is also willing to help them out without expecting anything in return. However, Wuffle tends to be naïve and too trusting, which often brings him unexpected trouble.",
           "Gender": "Male",
           "Species": "Wolf"
       },
       {
           "name": "Puipui",
           "desc": "A hedgehog who seems to be able to complain at anything he ever lays his eyes upon, though he never means any harm. Hot-headed and impatient, but surprisingly, Puipui is Wuffle's best friend and co-worker. It was Wuffle's idea that working on a farm might help Puipui with his anger management. Though honestly, he prefers eating and sleeping.",
           "img": "char-puipui.jpg",
           "Gender": "Male",
           "Species": "Hedgehog"
       }
   ]

This is not substantially different from the conventional format.
Because the characters file is specified with ``chars`` in the comic’s
configuration file, you can name it whatever you like, regardless of
format. (However, it is recommended that you use the ``.json`` extension
for JSON-formatted character files anyway, just to avoid confusion.) If
JSON-mode Springheel is unable to load a character file as JSON, it will
attempt to load it as YAML format instead; this will undoubtedly cause
issues if the *actual* problem is invalid JSON, so be careful.

About Pages
^^^^^^^^^^^

(new in version 7.0)

The index page contains descriptions of each comic on the site, but
you might want to include more detailed information---for example, to
credit type foundries or crowdfunding patrons, or just to talk about
the comic's history or plot with more than one line. For that, you can
set an About page, and it will appear in the site's top navigation.

To enable about pages, open up ``conf.ini`` and set ``about = True``.
Then open the ``.conf`` file(s) for the comic(s) you want to describe.
Define the ``about`` block like thus:

.. code-block:: yaml

    about = This is an example of the about page system.\nYou can add multiple lines of text.

Building produces ``about.html``, which contains blocks for each comic
on the site (including their banners and summaries from the index, so
you don't have to repeat the information from the latter). The example
above would generate a block like this:

.. code-block:: html

    <h2>[comic title]</h2>
    <img src="[comic banner]" alt="">
    <p class="author">by [author]</p>
    <p>[index summary]</p>
    <p>This is an example of the about page system.</p>
    <p>You can add multiple lines of text.</p>

You can also use some HTML, although it gets sanitized with
``html-sanitizer``. Note that lines are only wrapped in paragraph tags
if no HTML tags are present, so you'll have to add them manually in
this case.

.. code-block:: yaml

    about = <p>Helscome my wobsite. If you <span style="bold">want</span> to, you can use <a href="https://example.com">hyperlinks</a> and such.</p><script type="text/javascript" src="http://xn--ndu.xn--zckzah/some-malicious-script.js"></script>

Results in:

.. code-block:: html

    <h2>[comic title]</h2>
    <img src="[comic banner]" alt="">
    <p class="author">by [author]</p>
    <p>[index summary]</p>
    <p>Helscome my wobsite. If you <strong>want</strong> to, you can use <a href="https://example.com">hyperlinks</a> and such.</p>

The following tags are accepted:

-  ``a``
-  ``h1``
-  ``h2``
-  ``h3``
-  ``h4``
-  ``h5``
-  ``h6``
-  ``strong``
-  ``em``
-  ``p``
-  ``ul``
-  ``ol``
-  ``li``
-  ``br``
-  ``sub``
-  ``sup``
-  ``hr``
-  ``i``
-  ``b``
-  ``ruby``
-  ``rt``
-  ``rb``
-  ``date``
-  ``dl``
-  ``dt``
-  ``dd``
-  ``code``
-  ``del``
-  ``ins``

Trying to build
~~~~~~~~~~~~~~~

Whew! That was quite a bit of text without actually getting to *do*
much. For now, let’s just try building the site with the configurations
and preferences already present in the *Wuffle* sample pack’s files. It
should work out of the box, after all.

You run ``springheel-build`` in much the same way as
``springheel-init``:

On GNU/Linux, it’s ``$ springheel-build``

On Windows it’s
``<Your Python install path>\Scripts\springheel-build.exe``

Now just sit back and wait for the site to compile.

Checking the output
^^^^^^^^^^^^^^^^^^^

If ``springheel-build`` didn’t return any errors, your site *should*
appear in ``output/``.

Let’s look at the same strip as before. Here’s a navigation block, the
type that appears above and below the comic:

.. code-block:: html

   <ul class="cominavbox" id="topbox">
       <li><a href="wuffle_0001.html#topbox"><img src="arrows/plain_first.png" alt="First Page" /><br />First</a></li>
       <li><a href="wuffle_0003.html#topbox"><img src="arrows/plain_prev.png" alt="Previous Page" /><br />Previous</a></li>
       <li><a href="wuffle_0005.html#topbox"><img src="arrows/plain_next.png" alt="Next Page" /><br />Next</a></li>
       <li><a href="wuffle_0139.html#topbox"><img src="arrows/plain_last.png" alt="Last Page" /><br />Last</a></li>
   </ul>

(This one goes above the strip; the one underneath would have
``id="botbox"``.)

You don’t have to calculate any of this yourself; it’s generated
automatically!

Meanwhile, the .transcript will generate the following HTML:

.. code-block:: html

   <div role="region" id="transcript"><h2>Transcript</h2>
   <p class="action">(Wuffle paints a fence as Aunty Pinky looks on.)</p>
   <p class="line"><span class="charname">Wuffle</span>: 
   <span class="linedia">It's done, ma'am.</span></p>
   <p class="line"><span class="charname">Pinky</span>: 
   <span class="linedia">Thanks, sweetie.</span></p>
   <p class="action">(Pinky offers Wuffle a wad of money. He looks sheepish.)</p>
   <p class="line"><span class="charname">Wuffle</span>: 
   <span class="linedia">Oh, it's fine, ma'am. Please keep your money.</span></p>
   <p class="line"><span class="charname">Pinky</span>: 
   <span class="linedia">Oh, well. More for me.</span></p>
   <p class="action">(Pinky begins eating the money.)</p>
   </div>

Which will look something like this in the wild (again, with the Plain
style):

.. figure:: transcript-example.png
   :alt: Transcript example

   Nicely formatted, easy-to-parse dialogue and action.

From here on
~~~~~~~~~~~~

That should be that; you should have a usable site with all of
Springheel’s basic features. At this stage, you can fiddle around with
the settings, make your own themes or assets, and use the Wuffle files
as a sort of template for what your own comic files should look like.
When you have a site you’re satisfied with, you can upload it to your
webserver with the FTP/SSH/etc. client that you like best.

Updating
^^^^^^^^

Updating your Springheel site is simple. Just add the new strip(s) and
metadata files to ``input``, then run ``springheel-build`` again. Then
you can re-upload your newly-updated site and marvel at your RSS feed.

**NOTE:** Springheel rebuilds all pages in ``output/`` when you update –
if you’ve made any changes to those files, they’ll be overwritten.
Conversely (to reduce unnecessary disk rewrites), theme assets and
stylesheets are not altered if they exist in ``output/``. Delete
``output/assets`` and ``output/arrows`` if you do want to overwrite
these files.


