from imutils.video import VideoStream
from spread_and_send import create_spreadsheet
from imutils.video import FPS
import numpy as np
from flask import Response, url_for, request, redirect
from flask import render_template
from runapp import app
import threading
import werkzeug
import pickle
import imutils
import time
import cv2
import os

#initialize the output frame and a lock used to ensure thread-safe
#exchanges of the output frames (useful when multiple browsers/tabs)
#are viewing the stream
output_frame = None
lock = threading.Lock()
name, email, course = '', '', ''


#parse in the args value cus im tired of this shit !!!
# sorry for importing this here. its a huge reminder for me
from args import args

# load our serialized face detector from disk
print("[INFO] loading face detector...")
current_directory = os.path.dirname(__file__)
protoPath = "./face_detection_model/deploy.prototxt"
modelPath = "./face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
le_path = "./output/le.pickle"
recognizer_path = "./output/recognizer.pickle"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(recognizer_path, "rb").read())
le = pickle.loads(open(le_path, "rb").read())

# a list to store the detected faces class
detected_faces = list()


#initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        global name, email, course
        name = request.form.get('lecturer_name')
        email = request.form.get('email')
        course = request.form.get('course_code')
        return redirect(url_for('livestream'))
    else:
        return render_template('home.html')




@app.route("/livestream")
def livestream():
    return render_template('livestream.html', name=name, course=course)

def detect_f():
    global vs, output_frame, lock
    while True:
	# grab the frame from the threaded video stream
        frame = vs.read()

        # resize the frame to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > args["confidence"]:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                    (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                # draw the bounding box of the face along with the
                # associated probability
                proba_percent = proba * 100
                if (proba_percent > 75) and (name != "Unknown"):
                    text = "Welcome {}!".format(name)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                    detected_faces.append(name)
                    with lock:
                        output_frame = frame.copy()
                else:
                    text = "{}: {:.2f}%".format(name, proba_percent)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        (0, 0, 255), 2)
                    cv2.putText(frame, text, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    with lock:
                        output_frame = frame.copy()


def generate():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

#auto shutdown server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shut_down_nwanne():
    shutdown_server()
    return render_template('success.html', course=course, name=name)

if __name__ == '__main__':
    t = threading.Thread(target=detect_f)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True, use_reloader=False)

cv2.destroyAllWindows()
vs.stop()

unique_faces = np.unique(detected_faces)
create_spreadsheet(predicted_names=unique_faces, course_handler_email=email, lect=course)

