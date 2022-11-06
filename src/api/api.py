from flask import Flask, render_template, Response
import cv2
from keras.models import load_model
import time
from keras_preprocessing.image import img_to_array
from keras_preprocessing import image
import cv2
import numpy as np
import csv 
app = Flask("Flaskend")
sus_index = 0

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')
def analysis():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    classifier = load_model(r'model.h5')
    emotion_labels = ['Angry', 'Disgust', 'Fear',
                      'Happy', 'Neutral', 'Sad', 'Surprise']
    cap = cv2.VideoCapture(0)
    global sus_index
    Sec = 0
    Min = 0
    Check = 1
    Counter = 1
    overall_mood=[]
    last_time=0
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            labels = []
            label = 'a'
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces1 = face_cascade.detectMultiScale(gray)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces1:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (48, 48),
                                      interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    label = emotion_labels[prediction.argmax()]
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position,
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    overall_mood.append(label)
                    print(label)
                else:
                    cv2.putText(frame, 'No Faces', (30, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey),
                                  (ex+ew, ey+eh), (0, 255, 0), 2)

            if len(faces) > 0:

                Sec += 0.1
                last_time=Sec
                print(str(Min) + " Mins " + str(Sec) + " Sec ")

                cv2.putText(frame, "Time: " + str(Min) + " Mins " + str(Sec) + " Sec ",
                            (0, frame.shape[0] - 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0, 0, 255), 1)
                cv2.putText(frame, "Number of faces detected: " + str(
                    faces.shape[0]), (0, frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0, 0, 255), 1)

                time.sleep(0.1)
                if Sec == 60:
                    Sec = 0
                    Min += 1
                    print(str(Min) + " Minute")

                if Min == 2:
                    # The person has spent more than 2 minutes in the ATM Premise
                    sus_index += 1
                    print("Alert")
                    if Check == 1:
                        sus_index += 1
                        print("Suspicious activity detected inside ATM.")
                        Check += 1

            if len(faces) > 3 and Counter == 1:
                # first form of Suspicion is detected
                print("Suspicious activity detected inside ATM.")
                Counter += 1
                sus_index += 1

            if len(faces) == 0:
                # no one is using the atm/bank
                print('No face detected')
                if(last_time>=2 ):
                    avg_mood = max(set(overall_mood), key=overall_mood.count)
                    row=[[int(last_time),"State of Atm","Coustomer details",avg_mood,sus_index]]
                    filename = "moodanalytics.csv"
                    with open(filename, 'a') as csvfile: 
                        # writing in the csv file for further data analytics
                        csvwriter = csv.writer(csvfile)  
                        csvwriter.writerows(row)
                #resetting the array
                overall_mood=[]
                last_time =0
                sus_index=0
                cv2.putText(frame, "No face detected ", (0,
                            frame.shape[0] - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0, 0, 255), 1)
                Sec = 0
                Min = 0
            # Checking for the suspicion index limit and feeding it into anoter sequence to inform authorities
            if(sus_index >= 5):
                print("Suspicion Limit reached,Authorities informed")
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()

@app.route('/mood')
def moodfeed():
    return Response(analysis(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()
