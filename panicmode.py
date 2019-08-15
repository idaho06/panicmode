#!/usr/bin/env python3
# coding:utf-8

import svgwrite
from svgwrite import cm, mm
from wand.api import library
import wand.color
import wand.image
from datetime import datetime, timedelta

# Filename of png
prefix = ''
filename = prefix + 'panicmode.png'

# Your birthday goes here
d1 = datetime(year=1978, month=11, day=14)

# Time calculations
years = 82
weeks_per_year = 52
extra_week_per_year = 6
d2 = datetime.now()
monday1 = (d1 - timedelta(days=d1.weekday()))
monday2 = (d2 - timedelta(days=d2.weekday()))
lived_weeks = (monday2 - monday1).days / 7
# print(lived_weeks)

box_width = 2
box_margin = 1
xoffs = 1
yoffs = 1

dwg = svgwrite.Drawing(filename="test.svg", size=("25.5cm", "16.5cm"))
# dwg = svgwrite.Drawing(filename="test.svg", size=('2880','1800'))
# dwg = svgwrite.Drawing(filename="test.svg", size=('100%','100%'))

# Boxes drawing
week_number = 0
for year in range(1, years + 1):
    if year % extra_week_per_year == 0:
        weekoffset = 2
    else:
        weekoffset = 1
    for week in range(1, weeks_per_year + weekoffset):
        if week_number <= lived_weeks:
            rect_fill = 'black'
        else:
            rect_fill = 'white'
        # x pos depends on year
        xpos = (xoffs + (year * (box_width + box_margin))) * mm
        # y pos depends on week of the year
        ypos = (yoffs + (week * (box_width + box_margin))) * mm
        dwg.add(dwg.rect((xpos, ypos), (box_width * mm, box_width * mm), fill=rect_fill, stroke='gray'))
        week_number += 1

# Year numbers drawing
for year in range(1, years + 1):
    xpos = (xoffs + (year * (box_width + box_margin))) * mm
    ypos = (yoffs + 2) * mm
    dwg.add(dwg.text(str(year),
                     insert=(xpos, ypos),
                     stroke='none',
                     fill='black',
                     font_size='2mm',
                     font_weight="bold",
                     font_family="Monospace"))

# Week numbers drawing?
for week in range(1, weeks_per_year + 1):
    pass

svgstring = dwg.tostring()
svg_blob = svgstring.encode('utf-8')
# print(svgstring)
# dwg.save()

with wand.image.Image() as image:
    with wand.color.Color('transparent') as background_color:
        library.MagickSetBackgroundColor(image.wand,
                                         background_color.resource)
    image.read(blob=svg_blob)
    image.format = 'png'
    image.save(filename=filename)
