from django.views.decorators import gzip
from django.http import StreamingHttpResponse

import cv2
import threading
import numpy as np




class VideoCamera(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/StreamFromCamWithDjango/stream/show/recog.xml')
        self.video = cv2.VideoCapture(0) #VideoStream(usePiCamera = True).start()
        self.grabbed, self.frame = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #resize the image
        width = int(image.shape[1] * 50/100)
        height = int(image.shape[0] * 50/100)
        dsize = (width, height)
        image = cv2.resize(image, dsize)
        
        faces = self.face_cascade.detectMultiScale(image, 1.1, 5)
        print("Found " + str(len(faces)) + " face(s)")
        
        for (x,y,w,h) in faces:
                cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,0), 2)
        
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()
            
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass