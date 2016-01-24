#!/usr/bin/env python

import sys

from base import CubeLights

if len(sys.argv) > 1:
    if len(sys.argv) != 4:
        print "usage: cube.py [width depth height]"
    width =  sys.argv[1]
    depth =  sys.argv[2]
    height = sys.argv[3]
elif len(sys.argv) == 1:
    width = 12
    depth = 8
    height = 60
else:
    raise Error("Not possible?!")


class CubeLightsLayout(CubeLights):
  def __init__(self):
    super(CubeLightsLayout, self).__init__(width, depth, height)

  def GenerateLayout(self):
    points = []
    for y in range(self.depth):
      for x in range(self.width):
        for z in range(self.height):
          points.append(
              (x / self.xd - self.xl / 2.0,
               y / self.yd - self.yl / 2.0,
               z / self.zd - self.zl / 2.0))

    points.reverse()

    lines = []
    for p in points:
      lines.append(
          '  {"point": [%.2f, %.2f, %.2f]}'
          % (p[0] * 4.0, p[1] * 4.0, p[2] * 4.0))

    f = open(sys.argv[0] + '.json', 'w')
    f.write('[\n' + ',\n'.join(lines) + '\n]')
    f.close()

CubeLightsLayout().GenerateLayout()
