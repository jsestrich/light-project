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
            'amplitude': 0.8,
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
            'amplitude': 0.8,
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
            'amplitude': 0.8,
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

while True:
  pos = index * speed
  for w in range(width):
      for d in range(depth):
          red = DualWaveValue(w + pos, d + pos, prop['red'])
          green = DualWaveValue(w + pos, d + pos, prop['green'])
          blue = DualWaveValue(w + pos, d + pos, prop['blue'])
          for h in range(height):
              i = d * width * height + w * height + h
              pixels[i] = (
                  ToPixelLevel(h, red),
                  ToPixelLevel(h, green),
                  ToPixelLevel(h, blue)
                  )

  client.put_pixels(pixels)
  index += 1
