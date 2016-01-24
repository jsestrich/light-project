#!/usr/bin/env python

# Open Pixel Control client: All lights to solid white

import math, opc, random, time

numLEDs = 6000
client = opc.Client('localhost:8080')

staticpts = 1000
index = 0
while True:
    pixels = [ (0,0,0) ] * numLEDs
    staticpts = int(500 * (math.sin(index * .1) + 1.0))
    for i in range(staticpts):
        pixels[random.randint(0, numLEDs - 1)] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    client.put_pixels(pixels)
    time.sleep(1/60.0)
    index += 1
