#!/usr/bin/env python

import opc, time, math, random

numLEDs = 6000
client = opc.Client('localhost:8080')

pixels = [(0, 0, 0)] * numLEDs
index = -1
speed = 1.8
while True:
  pos = index * speed
  for i in range(0, numLEDs):
    level = i % 60
    lvl = math.fabs(level - pos)
    if (lvl <= 1):
      lvl = 1 - lvl
      pixels[i] = (255 * lvl, 255 * lvl, 255 * lvl)
    else:
      pixels[i] = (0, 0, 0)
  client.put_pixels(pixels)
  index += 1
  if (index * speed > 61):
    index = -1
