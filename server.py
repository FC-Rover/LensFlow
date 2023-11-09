#!/usr/bin/env python
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import cv2
import syslog
import traceback
import numpy as np

# Define a counter metric
counter_metric = Counter('ramin_image_stream_calls_total', 'Total calls to ramin image stream (counter)')

__info = {
    'name': 'Ramin Dehghan',
    'email': 'online@wolog.org',
    'title': 'dev',
    'description': 'An applet to stream pi camera over http.'
}

info = __info

# Define logging service
def log(_priority, _message):
    syslog.syslog(_priority, _message)

application = Flask(__name__)

camera = cv2.VideoCapture(0)

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
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@application.route('/video')
def video_feed():
    counter_metric.inc()
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    application.run()

if __name__ == '__main__':
    main()

