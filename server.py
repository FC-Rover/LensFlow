import atexit
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


def exit_handler():
    cam.stop_recording()
    cam.close()


cam = Picamera2()


def main():
    try:
        video_config = cam.create_video_configuration({"size": (1280, 720)})
        cam.configure(video_config)

        encoder = H264Encoder(1000000)
        output = FfmpegOutput("-f mpegts udp://0.0.0.0:10001?pkt_size=188&buffer_size=65535")
        cam.start_recording(encoder, output)
    finally:
        exit_handler()


atexit.register(exit_handler)

if __name__ == "__main__":
    main()
