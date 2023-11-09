#!/usr/bin/env python
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from time import sleep
import syslog
import traceback
from picamera2 import Picamera2
from PIL import Image
from io import BytesIO

# Define a counter metric
counter_metric = Counter('ramin_image_stream_calls_total', 'Total calls to ramin iamge stream (counter)')

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


# Define stream capture
def get_frame():
    # camera=cv2.VideoCapture(0)
    # success, frame = camera.read()
    # if not success:
    #     yield("No Image")
    # ret, buffer = cv2.imencode('.jpg', frame)
    # rame = buffer.tobytes()
    # camera.release()
    try:
        camera = Picamera2()
        config = camera.create_still_configuration()
        camera.configure(config)
        camera.start()
        sleep(2)
        image = BytesIO()
        camera.capture_file(image, format='jpeg')
        sleep(2)
        camera.stop()
        camera.stop_preview()
        camera.close()
        image.seek(0)
        # image = Image.open(image)
    except Exception as e:
        log(syslog.LOG_ERR, str(traceback.format_exc()))
        log(syslog.LOG_ERR, str(type(e)))
        log(syslog.LOG_ERR, str(e.args))
        log(syslog.LOG_ERR, str(e))
        yield (type(e) + '\n' + str(e.args) + '\n' + str(traceback.format_exc()))
    finally:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image.read() + b'\r\n')


application = Flask(__name__)


@application.route('/')
def index():
    counter_metric.inc()
    return "Functional"


# Show info
@application.route('/api/info', methods=['GET'])
def get_info():
    # Increase counter to
    counter_metric.inc()
    return jsonify(info)


# Provide dummy metrics for prometheus
@application.route('/metrics')
def metrics():
    # Generate the latest metrics in Prometheus format
    prometheus_metrics = generate_latest()
    return Response(prometheus_metrics, mimetype=CONTENT_TYPE_LATEST)


# Stream video
@application.route('/video')
def video():
    counter_metric.inc()
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    application.run()


if __name__ == '__main__':
    application.run()
