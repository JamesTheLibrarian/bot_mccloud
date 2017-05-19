# bot_mccloud

Scripts and resource files supporting the [@bot_mccloud](https://twitter.com/bot_mccloud) Twitter bot, which tweets random panels from Scott McCloud's *[Understanding Comics](http://scottmccloud.com/2-print/1-uc/)*.

The scripts found in this repository are used to automatically divide up each page of the book into individual panels. They assume your working directory contains all of the following:

* A `raw/` directory containing PNGs of the book's pages, one page per file.
* An empty `thresholded/` directory, to hold [thresholded](https://en.wikipedia.org/wiki/Thresholding_(image_processing)) versions of the page images (which are easier to programmatically analyze). This directory is populated when we run the `threshold.py` script, and its contents are then used by the `panelize.py` script.
* An empty `panels/` directory, to hold the final output panel files. This directory is populated when we run the `panelize.py` script.

It's also assumed that you have [ImageMagick](https://www.imagemagick.org) and [Pillow](https://python-pillow.org) installed.

To use the scripts, set up your working directory as described. Then run the `threshold.py` script, which will iterate over the images in the `raw/` directory and use ImageMagick to create a thresholded version of each one. Once that script finishes doing its thing, you can run `panelize.py` to separate out the individual panels from each page. If you have more than a handful of images, this will probably take a while!

I've only tested this on a particular scanned version of *Understanding Comics*, but in theory the same general approach – and maybe even these specific scripts! – could work equally well for a wide variety of comics.
