#!/usr/bin/env python

import opc, time, math, random

width = 12
depth = 8
height = 60
numLEDs = width * depth * height

client = opc.Client('localhost:8080')

line_width = 2.0
pixels = [(0, 0, 0)] * numLEDs
index = 0
speed = .1
prop = {
    'red': {
        'x': {
            'offset': 0,
            'period': .25,
            'amplitude': 0.4,
        },
        'y': {
            'offset': 0,
            'period': .25,
            'amplitude': 0.2,
        },
    },
    'green': {
        'x': {
            'offset': 0,
            'period': 0.5,
            'amplitude': 0.4,
        },
        'y': {
            'offset': 0,
            'period': .25,
            'amplitude': 0.2,
        },
    },
    'blue': {
        'x': {
            'offset': 0,
            'period': 1.0,
            'amplitude': 0.4,
        },
        'y': {
            'offset': 0,
            'period': .25,
            'amplitude': 0.2,
        },
    },
}

def WaveValue(x, prop):
    return prop['amplitude'] * (math.sin(x * prop['period'] + prop['offset'])) / 2.0

def DualWaveValue(x, y, prop):
    return WaveValue(x * 2 * math.pi / width, prop['x']) + WaveValue(y * 2 * math.pi / depth, prop['y'])

def ToPixelLevel(h, level):
    dist = min(line_width, math.fabs((h - height / 2) - level * height))
    return (line_width - dist) * 255

def Clamp(v, maxV):
    v += maxV
    v = v % (2 * maxV)
    v -= maxV
    return v

indexW = 0
indexD = 0
indexH = 0
while True:
  for w in range(width):
      for d in range(depth):
          for h in range(height):
              i = d * width * height + w * height + h
              red = abs(int( Clamp(indexW + w, width) * 1.0 / width * 255))
              green = abs(int( Clamp(indexD + d, depth) * 1.0 / depth * 255))
              blue = abs(int( Clamp(indexH + h, height) * 1.0 / height * 255))
	      pixels[i] = (red, green, blue)

  client.put_pixels(pixels)
  indexW = Clamp(indexW + .1 * width, width)
  indexD = Clamp(indexD + .1 * depth, depth)
  indexH = Clamp(indexH + .1 * height, height)
  time.sleep(0.05)
