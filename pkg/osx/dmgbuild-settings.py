# -*- coding: utf-8 -*-
#
# dmgbuild settings file
#
# Python 2.7 syntax
#
# Defines expected:
#
#     pkg      path to pkg file to include
#     readme   path to readme to include
#

from __future__ import absolute_import, division, unicode_literals
import os

# .. Basics ...................................................................

# Volume format (see 'hdiutil create -help')
format = 'UDBZ' # bzip2-compressed image
size = '1M'
files = [defines[key] for key in ('pkg', 'readme')]

# Where to put the icons
icon_locations = dict((os.path.basename(path), (200 * (i + 1), 100))
                      for i, path in enumerate(files))

# .. Window configuration ......................................................

# Background
#
# This is a STRING containing any of the following:
#
#    #3344ff          - web-style RGB color
#    #34f             - web-style RGB color, short form (#34f == #3344ff)
#    rgb(1,0,0)       - RGB color, each value is between 0 and 1
#    hsl(120,1,.5)    - HSL (hue saturation lightness) color
#    hwb(300,0,0)     - HWB (hue whiteness blackness) color
#    cmyk(0,1,0,0)    - CMYK color
#    goldenrod        - X11/SVG named color
#    builtin-arrow    - A simple built-in background with a blue arrow
#    /foo/bar/baz.png - The path to an image file
#
# The hue component in hsl() and hwb() may include a unit; it defaults to
# degrees ('deg'), but also supports radians ('rad') and gradians ('grad'
# or 'gon').
#
# Other color components may be expressed either in the range 0 to 1, or
# as percentages (e.g. 60% is equivalent to 0.6).
background = 'rgb(0.21, 0.63, 0.98)'

# Window position in ((x, y), (w, h)) format
window_rect = ((100, 100), (600, 400))

# .. Icon view configuration ..................................................

label_pos = 'bottom' # Position icon labels on the bottom
text_size = 12
icon_size = 72

# IMPORTANT: Don't use a grid_spacing over 100, else backgrounds break on
# Yosemite. We are leaving it out right now to let it become the default.
#
# See here:
# https://bitbucket.org/al45tair/mac_alias/issue/2/yosemite-has-changed-the-alias-format
# https://bitbucket.org/al45tair/dmgbuild/issue/4/background-images-not-working-on-yosemite
