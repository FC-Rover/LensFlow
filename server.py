#!/usr/bin/env python
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from time import sleep
from picamera2 import Picamera2
from io import BytesIO

# Define a counter metric
counter_metric = Counter('ramin_image_stream_calls_total', 'Total calls to ramin image stream (counter)')

__info = {
    'name': 'Ramin Dehghan',
    'email': 'online@wolog.org',
    'title': 'dev',
    'description': 'An applet to stream pi camera over http.'
}

info = __info


application = Flask(__name__)

# Init camera
camera = Picamera2()
config = camera.create_still_configuration()
camera.configure(config)
image = BytesIO()


@application.route('/')
def index():
    counter_metric.inc()
    return "Functional"


# Show info
@application.route('/api/info', methods=['GET'])
def get_info():
    # Increase counter
    counter_metric.inc()
    return jsonify(info)


# Provide dummy metrics for prometheus
@application.route('/metrics')
def metrics():
    # Generate the latest metrics in Prometheus format
    prometheus_metrics = generate_latest()
    return Response(prometheus_metrics, mimetype=CONTENT_TYPE_LATEST)


# Stream video
def generate_frames():
    try:
        camera.start()
        sleep(1)
        while True:
            camera.capture_file(image, format='jpeg')
            image.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image.read() + b'\r\n')
    finally:
        camera.stop()
        camera.stop_preview()
        camera.close()


@application.route('/video')
def video_feed():
    counter_metric.inc()
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    application.run()


if __name__ == '__main__':
    main()
