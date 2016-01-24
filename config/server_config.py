#!/usr/bin/env python
import sys, json

debug = False

# serials[y][x]
serials = [
  [["HJTRXHPHHNYBILSF", "OEISOQWKRDCBOROV"], ["KEEAISWEJTITSNSH", "RNXTVHSQVJUPIPSH"], ["KGYCGYSMTDSDKTQH", "ECSYOIMYTDYJCTCN"]],
#  [["HJTRXHPHHNYBILSF", "OEISOQWKRDCBOROV"], ["KEEAISWEJTITSNSH", "RNXTVHSQVJUPIPSH"], ["d", "d"]],
#  [["KGYCGYSMTDSDKTQH", "ECSYOIMYTDYJCTCN"], ["d", "d"],                               ["d", "d"]],
]

width = len(serials[0])
depth = len(serials)

# 2  3  6  7
# 0  1  4  5

def FadecandyDevice(x, y, front, serial):
    start_row1 = x * 4 * 60 + (y * 4 + (0 if front else 2)) * (width * 4 * 60)
    start_row2 = x * 4 * 60 + (y * 4 + (1 if front else 3)) * (width * 4 * 60)
    if debug:
        print x, y, front, start_row1, start_row2
    return {
        "type": "fadecandy",
        "comment": "%d-%d-%s" % (x, y, "front" if front else "back"),
        "serial": serial,
        "map": [
            [ 0, start_row1 +   0,   0, 60 ],
            [ 0, start_row1 +  60,  64, 60 ],
            [ 0, start_row1 + 120, 256, 60 ],
            [ 0, start_row1 + 180, 320, 60 ],
            [ 0, start_row2 +   0, 128, 60 ],
            [ 0, start_row2 +  60, 192, 60 ],
            [ 0, start_row2 + 120, 384, 60 ],
            [ 0, start_row2 + 180, 448, 60 ]
        ]
    }

config = {
  "listen": [None, 8080],
  "verbose": True,
    "color": {
    "gamma": 2.5,
      "whitepoint": [1.0, 1.0, 1.0]
  },
  "comment": "unit{front,back}-unit{left,center,right}-subunit{front,back}",
  "devices": [
    {
      "type": "gl_server",
      "port": 8888,
      "map": [
        [ 0, 0, 0, width * depth * 16 * 60 ]
      ]
    }
  ]
}

for x in range(width):
    for y in range(depth):
        config["devices"].append(FadecandyDevice(x, y, front=True, serial=serials[y][x][0]))
        config["devices"].append(FadecandyDevice(x, y, front=False, serial=serials[y][x][1]))

config_string = json.dumps(config, sort_keys=True, indent=2)
filename = sys.argv[0] + '.json'
f = open(filename, 'w')
f.write(config_string)
f.close()
if debug:
    print config_string
    print width, depth
print "Successfully generated %s" % filename
