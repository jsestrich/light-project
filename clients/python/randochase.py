#!/usr/bin/env python

import opc, time, math, random

numLEDs = 6000
client = opc.Client('localhost:8080')

pixels = [(0, 0, 0)] * numLEDs

for p in range(numLEDs):
  bits = random.getrandbits(3)
  if bits == 0:
    pixels[p] = (random.getrandbits(8),
                 random.getrandbits(8),
                 random.getrandbits(8))
  else:
    pixels[p] = (0, 0, 0)


while True:
  for i in range(numLEDs - 1, 0, -1):
    pixels[i] = pixels[i - 1]
  bits = random.getrandbits(3)
  if bits == 0:
    pixels[0] = (random.getrandbits(8),
                 random.getrandbits(8),
                 random.getrandbits(8))
  else:
    pixels[0] = (0, 0, 0)

  time.sleep(1.0 / 40)
  client.put_pixels(pixels)
