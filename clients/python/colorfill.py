#!/usr/bin/env python

import math, sys

from multiprocessing import Pool

from animation import CubeAnimator

white = (255, 255, 255)
black = (0, 0, 0)

## def SetPixelA(index, x, y, z, px, py, pz):
##   print "(%d, %d, %d) == (%f, %f, %f)" % (x, y, z, px, py, pz)

## def SetPixelB(index, x, y, z, px, py, pz):
##   if (index % numLEDs) == frame_index:
##     pixels[index] = white
##   else:
##     pixels[index] = black

## def Distance(p1, p2):
##   result = 0
##   for i in range(len(p1)):
##     result += math.pow(p2[i] - p1[i], 2)
##   return math.sqrt(result)

## def SetPixelC(index, x, y, z, px, py, pz):
##   pixels[x * depth * height
##          + y * height
##          + z] = (255 * (xl - px) / xl,
##                  255 * (yl - py) / yl,
##                  255 * (zl - pz) / zl)

## period = xl / (2 * math.pi)
## speed = 1.0 / fps
## def SetPixelD(index, x, y, z, px, py, pz):
##   ratio = 1 + math.sin((px + speed*frame_index) / period)
##   color = 255 * ratio / 2.0
##   pixels[x * depth * height
##          + y * height
##          + z] = (0, color, 0)


if len(sys.argv) != 5:
    print "usage: colorfill.py fps width depth height"
    sys.exit(1)

prog = CubeAnimator(fps=int(sys.argv[1]),
                    width=sys.argv[2], depth=sys.argv[3], height=sys.argv[4])

period_x = prog.xl / (2 * math.pi)
speed_x = 1.0 / prog.fps
period_y = prog.yl / (2 * math.pi)
speed_y = 0.9 / prog.fps
period_z = prog.zl / (2 * math.pi)
speed_z = 0.8 / prog.fps

def SetPixel(args):
    return SetPixelInner(*args)

def SetPixelInner(pixel_index, x, y, z, px, py, pz, frame_index=0):
    ratio_x = 1 + math.sin((px + speed_x * frame_index) / period_x)
    ratio_y = 1 + math.sin((py + speed_y * frame_index) / period_y)
    ratio_z = 1 + math.sin((pz + speed_z * frame_index) / period_z)
    color_x = 255 * ratio_x / 2.0
    color_y = 255 * ratio_y / 2.0
    color_z = 255 * ratio_z / 2.0
    return (color_x, color_y, color_z)

pool = Pool(processes=4)

prog.Run(pool, SetPixel)
