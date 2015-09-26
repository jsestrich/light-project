import sys

strip_density = None
width = None
depth = None
height = None
xd = None
yd = None
zd = None
xl = None
yl = None
zl = None
total_leds = None

class CubeLights(object):
    def __init__(self, width, depth, height):
        self.strip_density = 30
        self.width = int(width)
        self.depth = int(depth)
        self.height = int(height)
        self.xd = 9 / 2.0
        self.yd = self.xd
        self.zd = 59 / 2.0
        self.xl = (self.width - 1) / self.xd
        self.yl = (self.depth - 1) / self.yd
        self.zl = (self.height - 1) / self.zd
        self.total_leds = self.width * self.depth * self.height
        print self.__str__()

    def __str__(self):
        result = "xd = %f, yd = %f, zd = %f\n" % (self.xd, self.yd, self.zd)
        result += "xl = %f, yl = %f, zl = %f\n" % (self.xl, self.yl, self.zl)
        result += "w = %d, d = %d, h = %d\n" % (self.width,
                                                self.depth,
                                                self.height)
        result += "total_leds = %d" % self.total_leds
        return result

