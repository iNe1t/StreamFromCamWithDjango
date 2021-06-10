from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from picamera import PiCamera
import cv2
import threading
#раскоментить и протестировать
# import io
# import picamera
# import cv2
# import numpy

# #Create a memory stream so photos doesn't need to be saved in a file
# stream = io.BytesIO()

# #Get the picture (low resolution, so it should be quite fast)
# #Here you can also specify other parameters (e.g.:rotate the image)
# with picamera.PiCamera() as camera:
#     camera.resolution = (320, 240)
#     camera.capture(stream, format='jpeg')

# #Convert the picture into a numpy array
# buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

# #Now creates an OpenCV image
# image = cv2.imdecode(buff, 1)

# #Load a cascade file for detecting faces
# face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')

# #Convert to grayscale
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# #Look for faces in the image using the loaded cascade file
# faces = face_cascade.detectMultiScale(gray, 1.1, 5)

# print "Found "+str(len(faces))+" face(s)"

# #Draw a rectangle around every found face
# for (x,y,w,h) in faces:
#     cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

# #Save the result image
# cv2.imwrite('result.jpg',image)

class VideoCamera(object):
    def __init__(self):
        camera = PiCamera()
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


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