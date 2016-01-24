#!/usr/bin/env python

import opc, time, math, random

def GetColor():
  return (random.getrandbits(8),
          random.getrandbits(8),
          random.getrandbits(8))

strands = 12
numLEDs = strands * 60
client = opc.Client('localhost:8080')

numDrops = 150
drops = []
for i in range(0, numDrops):
  drops.append({'strand': random.randint(0, strands - 1),
                'start': random.randint(0, 59),
                'speed': random.randint(100, 400) / 100.0,
                'color': GetColor()})

index = 0;
while True:
  pixels = [(0, 0, 0)] * numLEDs
  for drop in drops:
    pos = (index - drop['start']) / drop['speed']
    if pos < 59:
      pixels[drop['strand'] * 60 + int(math.ceil(pos))] = drop['color']
      pixels[drop['strand'] * 60 + int(math.floor(pos))] = drop['color']
    else:
      drop['strand'] = random.randint(0, strands - 1)
      drop['color'] = GetColor()
      drop['start'] = index
      drop['speed'] = random.randint(100, 400) / 100.0
  index += 1
  time.sleep(1.0 / 300)
  client.put_pixels(pixels)
