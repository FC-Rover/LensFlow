#!/usr/bin/env python3

import atexit
from time import sleep
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


def exit_handler():
    cam.stop_recording()
    cam.close()


atexit.register(exit_handler)
cam = Picamera2()


def main():
    try:
        video_config = cam.create_video_configuration({"size": (1280, 720)})
        cam.configure(video_config)

        encoder = H264Encoder(1000000)
        output = FfmpegOutput("-f flv rtmp://localhost/live/stream")
        cam.start_recording(encoder, output)
        # /var/snap/lens-flow/common/var/www/html/camera/dash/stream.mpd
        while True:
            sleep(10)
    finally:
        exit_handler()


if __name__ == "__main__":
    main()
