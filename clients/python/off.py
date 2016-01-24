#!/usr/bin/env python

# Open Pixel Control client: All lights to solid white

import opc, time

numLEDs = 6000
client = opc.Client('localhost:8080')

black = [ (0,0,0) ] * numLEDs
client.put_pixels(black)
