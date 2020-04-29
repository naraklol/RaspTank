# HELPER CLASS

import io
import logging
import socketserver
from threading import Condition
from http import server


# Static HTML page to display the live stream
PAGE="""\
<html>
    <head>
        <title>RaspTank</title>
    </head>
    <body>
        <center><h1>RaspTank Camera</h1></center>
        <center><img src="stream.mjpg" width="640" height="480"></center>
    </body>
</html>
"""


# StreamingOutput class
# Stores a buffer with the frames of the stream
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

        self.capture = False
        self.capture_filename = ''

    def capture_from_stream(self, filename):
        self.capture = True
        self.capture_filename = filename

    # Callback function by picamera to add a new frame to the buffer
    def write(self, buf):

        # New frame, copy the existing buffer's content and notify all
        # clients it's available (\xff\xd8 is the start code for jpg)
        if buf.startswith(b'\xff\xd8'):

            # check if the current frame needs to be captured
            if self.capture:
                with open(self.capture_filename, 'wb') as file:
                    file.write(buf)
                self.capture = False
                self.capture_filename = ''

            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


# StreamingHandlerClass
# Handles HTTP requests from a client
class StreamingHandler(server.BaseHTTPRequestHandler):
    # Connection from a client
    def do_GET(self):

        # default landing page, redirects to index
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()

        # main page with the HTML object from above
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        # streaming video file
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()

            # try sending the current frame
            try:
                while True:
                    with stream.condition:
                        stream.condition.wait()
                        frame = stream.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

            # return an exception
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


# StreamingServer class
# Runs the server on the pi that handles connections from clients
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


stream = StreamingOutput()
