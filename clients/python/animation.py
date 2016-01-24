import opc, time, math, random, sys

from base import CubeLights


class FPSQueue(object):
    def __init__(self, samples):
        self.samples = samples
        self.frames = [0] * samples
        self.pos = 0

    def RecordFrame(self, ts, pixel_count):
        self.frames[self.pos] = ts
        self.pos = (self.pos + 1) % self.samples
        if self.pos == 0:
            fps = (self.samples - 1) / self.GetTotalTime()
            print "%s fps (%f Mbps)" % (
                round(fps, 2),
                round(24 * pixel_count * fps / 1000000, 2))

    def GetFrameTime(self, index):
        return self.frames[index % self.samples]

    def GetTotalTime(self):
        return self.GetFrameTime(self.pos - 1) - self.GetFrameTime(self.pos)


class CubeAnimator(CubeLights):
    def __init__(self, fps, width, depth, height):
        super(CubeAnimator, self).__init__(width, depth, height)
        self.fps = int(fps)
        self.pixels = [(0, 0, 0)] * self.total_leds
        self.client = opc.Client('localhost:8080')
        self.fpsqueue = FPSQueue(int(fps))
        self.pixel_args = self.GeneratePixelArgs()

    def GeneratePixelArgs(self):
        result = []
        for x in range(self.width):
            for y in range(self.depth):
                for z in range(self.height):
                    pixel_index = (x * self.depth * self.height +
                                   y  * self.height +
                                   z)
                    px = x / self.xd
                    py = y / self.yd
                    pz = z / self.zd
                    result.append((pixel_index,
                        x,
                        y,
                        z,
                        px,
                        py,
                        pz))
        return result
        
    def Run(self, pool, set_pixel):
        frame_index = 0
        start_time = round(time.time())
        while True:
            next_frame_time = start_time + (frame_index / float(self.fps))
            now = time.time()
            self.fpsqueue.RecordFrame(now, len(self.pixels))
            wait_time = next_frame_time - now
            #print "frame %f %f %f" % (time.time(), next_frame_time, wait_time)
            if (wait_time > 0.0):
                time.sleep(wait_time)
            #else:
                #print "falling behind: %f" % wait_time
            self.RenderFrame(frame_index, pool, set_pixel)
            frame_index += 1

    def RenderFrame(self, frame_index, pool, set_pixel):
        args = [(pixel_arg + (frame_index, )) for pixel_arg in self.pixel_args]
        self.pixels = pool.map(set_pixel, args, chunksize=len(self.pixels)/8)
#        for pixel_arg in self.pixel_args:
#            joined_args = pixel_arg + (frame_index, )
#            self.pixels[pixel_arg[0]] = self.SetPixel(*joined_args)
        self.client.put_pixels(self.pixels)
