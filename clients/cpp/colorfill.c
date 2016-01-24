#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>

#include "opc.h"

int64_t width, depth, height;
double xd;
double yd;
double zd;
double xl;
double yl;
double zl;
int64_t total_leds;
u8 channel;

int64_t fps;
double period_x;
double speed_x;
double period_y;
double speed_y;
double period_z;
double speed_z;

void render_pixel(
    pixel* p, int64_t frame_index, int64_t pixel_index,
    int64_t x, int64_t y, int64_t z,
    double px, double py, double pz) {
  double ratio_x = 1 + sin((px + speed_x * frame_index) / period_x);
  double ratio_y = 1 + sin((py + speed_y * frame_index) / period_y);
  double ratio_z = 1 + sin((pz + speed_z * frame_index) / period_z);
  p->r = 255 * ratio_x / 2.0;
  p->g = 255 * ratio_y / 2.0;
  p->b = 255 * ratio_z / 2.0;
}

void render_frame(pixel* pixels, int64_t frame_index) {
  int64_t pixel_index = 0;
  int64_t x = 0, y = 0, z = 0;
  for (x = 0; x < width; x++) {
    for (y = 0; y < depth; y++) {
      for (z = 0; z < height; z++, pixel_index++) {
	render_pixel(pixels + pixel_index,
		     frame_index, pixel_index,
		     x, y, z,
		     x / xd, y / yd, z / zd);
      }
    }
  }
}

uint64_t now() {
  struct timeval result;
  gettimeofday(&result, NULL);
  return result.tv_sec * 1000000 + result.tv_usec;
}

void sleep_until(int64_t ts_usec) {
  int64_t sleeptime_usec = ts_usec - now();
  if (sleeptime_usec <= 0) {
    return;
  }
  struct timespec spec;
  spec.tv_sec  =  sleeptime_usec / 1000000;
  spec.tv_nsec = (sleeptime_usec % 1000000) * 1000;
  nanosleep(&spec, NULL);
}

struct fps_queue {
  int64_t samples;
  int64_t pos;
  int64_t *frames;
};

void record_frame(struct fps_queue* queue) {
  queue->frames[queue->pos++] = now();
  queue->pos %= queue->samples;
}

int64_t get_elapsed(struct fps_queue* queue) {
  int64_t previous = (queue->pos - 1 + queue->samples) % queue->samples;
  return queue->frames[previous] - queue->frames[queue->pos];
}

int main(int argc, char** argv) {
  width = 12, depth = 8, height = 60;
  xd = (width - 1) / 2.4;
  yd = (depth - 1) / 1.6;
  zd = (height - 1) / 2.0;
  xl = (width - 1) / xd;
  yl = (depth - 1) / yd;
  zl = (height - 1) / zd;
  total_leds = width * depth * height;
  channel = 0;

  fps = 60;
  period_x = xl / (2 * M_PI);
  speed_x = 1.0 / fps;
  period_y = yl / (2 * M_PI);
  speed_y = 0.9 / fps;
  period_z = zl / (2 * M_PI);
  speed_z = 0.8 / fps;

  pixel pixels[total_leds + 1];
  opc_sink s;

  if (argc < 2) {
    fprintf(stderr, "Usage: %s <server>[:<port>]\n", argv[0]);
    return 1;
  }

  s = opc_new_sink(argv[1]);

  int64_t frame_index = 0;
  int64_t start = now();
  struct fps_queue fpsq;
  int64_t frames[total_leds];
  fpsq.samples = fps;
  fpsq.pos = 0;
  fpsq.frames = frames;
  while (1) {
    sleep_until(start + 1000000 * frame_index / fps);
    render_frame(pixels, frame_index);
    if (!opc_put_pixels(s, channel, total_leds, pixels)) {
      break;
    }
    record_frame(&fpsq);
    if (fpsq.pos == 0) {
      double cur_fps = (fpsq.samples - 1) / (get_elapsed(&fpsq) / 1000000.0);
      printf("fps: %.2f  (%.2f Mbps)\n",
	     cur_fps, total_leds * 24 * cur_fps / 1000000.0);
    }
    frame_index++;
  }
  printf("fps: %f\n", frame_index / 5.0);
}
