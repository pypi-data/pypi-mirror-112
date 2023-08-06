Extending Springheel Sites
==========================

Springheel projects keep their own copies of the HTML templates
and translation strings used to generate pages. That means you have to
re-run ``springheel-init`` whenever the installed templates are
updated, but it also makes it possible to tweak the templates to add
new features. The phrase “HTML templates” in these instructions refers
to the following files in your project’s ``templates/`` directory:

-  ``archive-template.html`` (the template for archives and tag pages)
-  ``base-template.html`` (the basic template for comic pages)
-  ``chapter-template.html`` (the template for chapter-view pages)
-  ``characters-template.html`` (the template for character pages)
-  ``extras-template.html`` (the template for extras pages)
-  ``index-template.html`` (the template for the main page)

The local translation string file is located at ``templates/strings.json``
and is just a JSON file mapping strings in various languages, language
names, and Python variable names. You can edit this file to add new
languages, fix bad translations, or change the English terms used if
you desire (e.g. referring to chapters as "Books" or "Tomes" for flavor).
See the `Translation API documentation page <translation_api.html>`__
for specifics.

I’ll note at this juncture that I can’t provide support for the features
that rely on third-party products or services. I claim no responsibility
for making sure that your site and content comply with any particular
laws.

Favicons
--------

Creating “proper” favicons is a highly involved process (c.f. `A Crime
Called Favicon <https://meiert.com/en/blog/schmavicons/>`__). Until this
changes, I would recommend using an automated utility of some sort to
generate the icons and HTML snippets rather than crafting them all by
hand. There are plenty of online and command-line tools that can do so
at a variety of different price points.

Each template in ``templates/`` has a comment like
``<!-- Add favicon code here -->`` in its ``<head>`` matter. Just remove
that comment and replace it with the lines of markup from the icon tool
you used (most will probably begin with ``<link rel=``). Then place the
generated icons directly in ``output/``.

Analytics
---------

Before putting any kind of tracking on your site, read up on the
legality of user data collection and storage in your jurisdiction. There
may be strict limitations on things like what you track, how you do so,
and what you do with it, especially if some of your readers may be
minors.

For a static site, you’ll presumably want a JavaScript-based analytics
tool that doesn’t need a SQL database or the like to run, such as
`Simple Analytics <https://github.com/simpleanalytics/scripts>`__.
Depending on what you use and where you live, you may also want/need
additional libraries (such as `cookieBAR <https://cookie-bar.eu/>`__ or
an age checker).

The documentation for whatever specific libraries you use will be of
more use than anything I can tell you, but they’ll *probably* boil down
to including a line like
``<script src="[URL of some file ending in .js]"></script>`` in your
pages. Open up the HTML templates and stick each ``<script>`` element in
each one. If your installation instructions tell you to put it at a
particular location (e.g. in ``<head>`` or right before the ``</body>``
tag), do that. If they need extra CSS, add links to the stylesheets in
question in the same way.

Ads, Comments, and Share Buttons
--------------------------------

Most ad services provide you with a bit of JavaScript you’re supposed to
add to your pages, and there are plenty of static site-friendly choices
for comment systems (e.g. `Disqus <https://disqus.com/>`__,
`Isso <https://posativ.org/isso/>`__, and
`Commento <https://commento.io/>`__) and social buttons (e.g. `Private
Secure Share
Buttons <https://github.com/QuadrupleA/private-secure-sharing-buttons>`__
and `Social Minus Spying <https://ncase.me/SocialMinusSpying/>`__) that
similarly rely on small bits of JS.

As with analytics, just insert the ``<script>`` and such where your
service’s instructions tell you to, in the HTML templates for whatever
types of page you want it to control. For the particularly minimalist,
`Sharingbuttons.io <https://sharingbuttons.io/>`__ doesn’t even use
JavaScript; if it’s to your liking, add its HTML in
``base_template.html`` (between ``{bottom_nav}`` and
``<!--COMMENT AREA-->``, I daresay) and its CSS in
``themes/[your theme]/style.css``.

If you need a permalink, just use ``{url}`` – Springheel 6.0 and higher
will convert that to the full URL of the page at build time. Note that
this doesn’t do any URL encoding, but Springheel slugifies page
filenames anyway, so it’s unlikely to cause issues.

Advertising is untested, so be warned that some themes may look odd with
ads in certain places or orientations.

I will note that just because you *can* add comments to your site 
doesn't mean you *should*. Internet comment culture is not nice, and 
they're especially cruel to people who create things. Getting constant 
questions about when the next update will be is honestly the *best*-case 
scenario. Will you be able to handle that? What about people bugging you 
to put things they like in the comic, or take out things they don't? 
What about people acting just plain hateful, even violent, about both 
your work and you personally? Think carefully about the effects comments 
might have on your mental and physical health before you enable them.

Right-to-left Languages
-----------------------

Springheel does not set site language directionality automatically,
regardless of your ``<navdirection>`` setting. This is because some
languages use different directions for different things. For example,
modern Japanese text is written from left to right when it’s horizontal
(like most webpages), but first-previous-next-last navigation still goes
from right to left.

To make your site display all text from right to left, just open up your
HTML templates and add ``dir="rtl"`` to all ``<html>`` elements.
