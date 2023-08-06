Frequently Asked Questions
==========================

\* (Questions may or may not have been asked, let alone “frequently”)

Q. Must I include a transcript for every strip?
-----------------------------------------------

A. No, you don’t *have* to include any transcripts. You can absolutely
build a Springheel site without a single one. But it’s still **highly**
recommended. Without any searchable plain text for your comics:

-  You’ll take a huge hit to accessibility and SEO.
-  Readers will have a harder time looking up words or phrases they
   don’t know.
-  People looking for a specific strip based on a piece of remembered
   dialogue will have to just give up and hate you forever.

Q. I’m on a Mac and…
--------------------

A. I don’t use Apple products, so I can’t really provide support or
troubleshooting for them. Sorry.

Q. How do I fix the encoding errors when I run Springheel through the Windows command line?
-------------------------------------------------------------------------------------------

A. I’ve done my best to mitigate this, but it is a problem with some
older versions of Windows that I can’t really control. `Look up how to
enable Unicode in the command
line <https://duckduckgo.com/?q=windows+command+line+enable+unicode>`__
for your version of Windows, and that should fix it. (Updating Python
may also help.)

Q. The date format you use is weird!
------------------------------------

A. That’s not a question! But Springheel’s date format – a four-digit
year, two-digit month, and two-digit day, in that order – follows the
ISO 8601 specification for date display. I happen to personally like
this format, but that’s quite aside from the fact that it is the
official, internationally-recognized, unambiguous standard. (See also
`XKCD’s take on the matter <https://xkcd.com/1179/>`__.)

Q. Why is the text so big?
--------------------------

It’s more like other sites’ text is `too
small <https://blog.marvelapp.com/body-text-small/>`__. I’m *very*
nearsighted, so I designed the Springheel themes to display text at a
size I could personally read easily.

Q. Why doesn’t Springheel keep track of the time a comic was published, instead of just the date?
-------------------------------------------------------------------------------------------------

A. No matter what, there is going to be a gap between the listed time
and the time when it was uploaded to the server. I didn’t want to
pretend a degree of accuracy and precision that wasn’t actually there.

Q. Can you recommend a good web host?
-------------------------------------

A. I’m not too familiar with free hosting if that’s what you’re after.
But if you do have a hosting budget and are technically adept, I highly
recommend `NearlyFreeSpeech <http://nearlyfreespeech.net>`__ – their
pricing is very reasonable, their service is consistent (pretty much no
downtime in my experience), and they offer many useful services for the
privacy-conscious.

Q. Why don’t the navigation arrows come with hovered versions?
--------------------------------------------------------------

A. The conventional method for adding image hover effects is inflexible,
crufty, non-semantic, and inaccessible (c.f. `Notes on accessible CSS
image
sprites <https://developer.paciellogroup.com/blog/2012/08/notes-on-accessible-css-image-sprites/>`__),
and icon fonts are even worse (c.f. `Icon font
accessibility <https://fvsch.com/code/icon-font-a11y/>`__, `Ten reasons
we switched from an icon font to
SVG <http://ianfeather.co.uk/ten-reasons-we-switched-from-an-icon-font-to-svg/>`__,
`CSS generated content is not
content <http://www.karlgroves.com/2013/08/26/css-generated-content-is-not-content/>`__).
If there is a semantic, pure HTML+CSS solution that allows for alt text,
without setting a million exact ``px`` values or creating empty
non-semantic elements, I’m all ears.

At the very least, the “note”, “seasonal”, and “elemental” themes’
arrows change color on hover.

Q. Why doesn’t Springheel use JavaScript? If you used JS you could do <blah blah>…
----------------------------------------------------------------------------------

A. `JavaScript is
overused <https://eev.ee/blog/2016/03/06/maybe-we-could-tone-down-the-javascript/>`__
and often unnecessary. There is nothing wrong with plain old HTML
(especially for static text and images, as Springheel sites mostly are),
and anyone who tries to convince you that “it’s $year, your site MUST
have the flavor of the month!” is selling something.

JavaScript also poses numerous `security
hazards <https://arstechnica.com/security/2016/12/millions-exposed-to-malvertising-that-hid-attack-code-in-banner-pixels/>`__
and even `copyright
problems <https://www.gnu.org/philosophy/javascript-trap.html>`__.
Excessive JavaScript simply to make things “nicer” often blocks readers
with less CPU power, like those on mobile devices or older computers,
from even being able to view the site at all. And sometimes JavaScript
interferes with other controls – a script on a particular newspaper site
completely blocks all keyboard navigation (no Page Up/Down, space, arrow
keys, etc.), which is catastrophic for assistive technology users! I
wanted vanilla Springheel sites to be perfectly usable even with
JavaScript turned completely off.

If there’s some specific thing you want to do (as in the examples of
“extending Springheel” above) that JavaScript can solve, then feel free
to use it. Just please do a minimum amount of testing to make sure you
aren’t breaking some existing part of the browser.

Q. Does the “note” theme follow Material Design guidelines?
-----------------------------------------------------------

A. Nope!

Q. Filenames aren’t slugified correctly, or I get slugify-related build errors.
-------------------------------------------------------------------------------

A. Unfortunately, there are multiple Python modules that internally
refer to themselves as just “slugify” (e.g. ``awesome-slugify``,
``unicode-slugify``). If more than one “slugify” is installed, there is
no way to ensure that we have the one we want, and they’re all different
enough that bad things – ranging from minor annoyances to program
crashes – happen if “import slugify” calls up the wrong one.

To ensure that Springheel works correctly, you will need to either

1. install Springheel in a clean virtual environment, or
2. completely remove all “slugify” libraries but ``python-slugify``.
