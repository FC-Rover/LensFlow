#!/usr/bin/env python3

import atexit
from time import sleep
import socket
import pickle
import struct
import imutils
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput


def exit_handler():
    cam.stop_encoder()
    cam.stop_recording()
    cam.close()


atexit.register(exit_handler)
cam = Picamera2()

## Create server side sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname
hostip = socket.gethostbyname(hostname)
print("Host IP: ", hostip)
port = 10051
sock_addr = (hostip, port)
print("Socket Created")
# Bind socket to host
sock.bind(sock_addr)
print("Socket Bound")
# Listen
sock.listen(3)
print("Socket Now Listening")


def main():
    try:
        video_config = cam.create_video_configuration({"size": (1280, 720)})
        cam.configure(video_config)
        encoder = H264Encoder(1000000)
        # output = FfmpegOutput("-f flv rtmp://localhost/live/stream")
        while True:
            client_sock, addr = sock.accept()
            print("Connection From: ", addr)
            if client_sock:
                stream = sock.makefile("wb")
                encoder.output = FileOutput(stream)
                cam.start_encoder()
                cam.start()
                sleep(20)
                exit_handler()
                client_sock.close()
    finally:
        exit_handler()


if __name__ == "__main__":
    main()
