# MAKE SURE TO KILL THE ADEEPT SERVER CODE RUNNING
# Run the following command before staring this:
# sudo pkill python3

import stream
import picamera
import threading

# Camera Class
class Camera():

    # Initialize a new camera object
    def __init__(self):
        self.camera = picamera.PiCamera(resolution='640x480', framerate=24)
        self.streaming = False

        # stream parameters
        self.stream = stream.stream
        self.address = None
        self.server = None
        self.server_thread = None

    def capture(self, filename):
        if self.streaming:
            self.stream.capture_from_stream(filename)
        else:
            print('not programmed')

    # Starts a server that hosts the current camera stream
    # Can be accessed from the IP address of the pi within a web browser
    def start_stream(self):
        self.camera.start_recording(self.stream, format='mjpeg')
        try:
            self.address = ('', 8000)
            self.server = stream.StreamingServer(self.address, stream.StreamingHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever, args=())
            self.server_thread.start()
            self.streaming = True
        except:
            self.camera.stop_recording()

cam = Camera()
cam.start_stream()
while True:
    pass
