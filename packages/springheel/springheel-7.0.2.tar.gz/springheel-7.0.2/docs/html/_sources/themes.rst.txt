======
Themes
======

Defaults
--------

Springheel comes equipped with a whopping 33 default themes, in order to
match a wide variety of comic genres. Several of them contain alternate
“sub-themes”, bringing the practical total to 44. They’re all
written with `Sass <https://sass-lang.com/>`__, then compiled to a
Cascading Style Sheet. (This is done separately from the comic
generation process; Springheel does not contain a Sass parser.)

To use any of these themes, just enter its name as ``site_style`` in
``conf.ini``. Plain is the default.

If your site contains multiple comic series, you can even set individual
styles for each one; just set “theme” in that comic’s ``.conf`` to the
theme name you want.

These are the themes available by default:

plain
  An extremely simple theme. Uses no images.

dark
  A simple dark theme. Uses no images.

beach
  A relaxed and fun theme inspired by the blue ocean.

berryheart
  A cozy “country” theme with check prints and strawberries.

blacktea
  A refined and dainty theme with lace and black tea as the main motifs.

book
  An elegant theme inspired by hardbound books.

brandy
  A hard-boiled noir theme of stark light and darkness.

cherry
  A girly pink theme for shoujo dreamers.

city
  A dreamy, twinkly theme.

crystal
  A glittering, lovely, strange, and dark theme.

cute
  A cute, candy-themed pink and brown theme. Might be good for comics about sweets or children.

cyber
  A theme inspired by 90s cyberpunk.

elemental
  A theme based on the classical elements. **Requires configuration before use.**

  This theme comes in multiple sub-styles: water, fire, earth, air, spirit, ice, metal, wood, electricity.

  To use one, copy the desired substyle's CSS file to ``style.css``. (If you want to change to a different sub-style later, simply remove the current ``style.css`` and make another copy.)

fairy
  A fluffy theme with flowers and sparkles.

fantasy
  A lush theme with green, gems, and parchment, perfect for “high fantasy” comics.

fluff
  A fun and fuzzy theme to unleash your wild side.

garden
  A soothing floral theme. **Warning: large theme.**

gothic
  featuring blood, roses, and bloody roses.

haunted
  A slightly cute, slightly spooky theme inspired by haunted houses. Suited for comedic horror comics.

magiccircle
  A mysterious, fantastical theme. **Warning: large theme.**

meikai
  An eccentric, eclectic theme combining mysticism with machinery.

might
  A bold theme for comics about heroes who are super.

note
  A striking, modern theme, designed to look “native” on phones. Uses no images.

  This theme is specifically designed to be easily customized – check the comments near the top of the CSS file.

prayers
  A peaceful theme in the image of a Shinto shrine. Mostly included because fans of a certain scrolling-shooter game might prefer red-white over black. ^_-

revolution
  A dark theme with hearts, swords, and flowers (specifically roses, and lots of them) for those who want to live nobly and with style. **Warning: large theme.**

rock
  A theme with plenty of star power, perfect for comics involving three chords and cowboys of the rhinestone variety.

seasonal
  A theme you can change to match the seasons. **Requires configuration before use.**

  This theme comes in four sub-styles. They’re more or less the same, just with different colors and background images. To use one, copy one of the four (``spring.css``, ``summer.css``, ``autumn.css``, or ``winter.css``) to ``style.css``. (If you want to change to a different sub-style later, simply remove the current ``style.css`` and make another copy.)

showtime
  A dramatic theme based on theatrical staging.

staples
  An institutional theme suitable for stories about schools, offices, or similar settings.

starship
  A retro sci-fi theme with stars and metal.

steam
  A “steampunk” theme with plenty of gears.

sysadmin
  A no-nonsense monospaced theme for fighting in the eighties. Uses no images.

twothousand
  A theme inspired by typical comic site designs from the early 2000s. Uses no images.

western
  A rugged theme fit for a cowpoke.

Theme Sizes
-----------

This table lists the file sizes of each theme. Note that if your theme
contains subthemes, Springheel will copy all subthemes' assets. The
figure provided in the Total column assumes that you delete unused
theme assets manually.

=========== =================== ============= ==========
Theme Name  CSS/Asset Size      Arrows Size   Total Size
=========== =================== ============= ==========
beach       24 KiB              7.2 KiB       31.2 KiB
berryheart  8.4 KiB             7.7 KiB       16.1 KiB
blacktea    10.3 KiB            1.8 KiB       12.1 KiB
book        13.1 KiB            2.8 KiB       15.9 KiB
brandy      6.8 KiB             23.1 KiB      29.8 KiB
cherry      9.3 KiB             5.4 KiB       14.6 KiB
city        5.3 KiB             677 B         6 KiB
crystal     8.9 KiB             4.7 KiB       13.5 KiB
cute        6.7 KiB             4.5 KiB       11.3 KiB
cyber       6.6 KiB             7.9 KiB       14.5 KiB
dark        3.7 KiB             3.4 KiB       7.2 KiB
elemental   6.2–8.1 KiB each    2.5 KiB       8.7–10.5 KiB
fairy       12.7 KiB            14.1 KiB      26.8 KiB
fantasy     18.1 KiB            18.2 KiB      36.3 KiB
fluff       6.4 KiB             5.7 KiB       12 KiB
garden      63.4 KiB            17.7 KiB      81.1 KiB
gothic      14.7 KiB            19.2 KiB      33.9 KiB
haunted     18.8 KiB            22 KiB        40.9 KiB
magiccircle 74.7 KiB            15 KiB        89.7 KiB
meikai      11.8 KiB            7.8 KiB       19.5 KiB
might       5.9 KiB             8.2 KiB       14.1 KiB
note        7.2 KiB             3.5 KiB       10.7 KiB
plain       3.4 KiB             3.6 KiB       6.9 KiB
prayers     6.7 KiB             27.4 KiB      34.1 KiB
revolution  18.4 KiB            5.4 KiB       23.7 KiB
rock        8.7 KiB             22 KiB        30.6 KiB
seasonal    6.8–7.2 KiB each    1.6 KiB       8.4–8.8 KiB
showtime    19.5 KiB            6.7 KiB       26.3 KiB
staples     14.9 KiB            5.6 KiB       20.5 KiB
starship    8.3 KiB             684 B         9 KiB
steam       17.3 KiB            7.8 KiB       25 KiB
sysadmin    4.5 KiB             412 B         4.9 KiB
twothousand 8.1 KiB             4.4 KiB       12.5 KiB
western     9.5 KiB             15.6 KiB      25.1 KiB
=========== =================== ============= ==========

Customizing
-----------

If you’re OK with a default theme with some tweaks, make a backup copy
of that theme’s ``style.css`` (or its base .scss if you prefer) just in
case, then fiddle around with the CSS as much as you want. Springheel
copies the ``style.css`` file from your selected theme as part of the
generation process, so make sure to run it once you’re done.
