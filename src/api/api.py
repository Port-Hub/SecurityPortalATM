from flask import Flask, render_template, Response
import cv2
from keras.models import load_model
import time
from keras_preprocessing.image import img_to_array
from keras_preprocessing import image
import cv2
import numpy as np

app = Flask("Flaskend")
sus_index = 0

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')
# for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
def analysis():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    classifier =load_model(r'model.h5')
    emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
    cap = cv2.VideoCapture(0)
    global sus_index
    Sec = 0
    Min = 0
    Check = 1
    Counter = 1
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            labels = []
            label = 'a'
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces1 = face_cascade.detectMultiScale(gray)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces1:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = classifier.predict(roi)[0]
                    label=emotion_labels[prediction.argmax()]
                    label_position = (x,y)
                    cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    print(label)
                else:
                    cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)     

            if len(faces) > 0:  

                Sec += 1
                print(str(Min) + " Mins " + str(Sec) + " Sec ")

                cv2.putText(frame, "Time: " + str(Min) + " Mins " + str(Sec) + " Sec ", (0,frame.shape[0] -30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)
                cv2.putText(frame, "Number of faces detected: " + str(faces.shape[0]), (0,frame.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)    

                time.sleep(1)
                if Sec == 60:
                    Sec = 0
                    Min += 1
                    print(str(Min) + " Minute")

                if Min == 2:
                    sus_index +=1
                    print("Alert")
                    if Check == 1:
                        print("Suspicious activity detected inside ATM.")
                        Check += 1   

            if len(faces) > 3 and Counter == 1:
                print("Suspicious activity detected inside ATM.")
                Counter += 1
                sus_index +=1

                        
            if len(faces) == 0:

                print('No face detected')
                cv2.putText(frame, "No face detected ", (0,frame.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)        
                Sec = 0
                Min = 0
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break  
            frame = buffer.tobytes()    
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()     



def timepeopleCounter():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)

    Sec = 0
    Min = 0
    Check = 1
    Counter = 1

    while 1:
        success, img = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)     

            if len(faces) > 0:  

                Sec += 1
                print(str(Min) + " Mins " + str(Sec) + " Sec ")

                cv2.putText(img, "Time: " + str(Min) + " Mins " + str(Sec) + " Sec ", (0,img.shape[0] -30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)
                cv2.putText(img, "Number of faces detected: " + str(faces.shape[0]), (0,img.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)    

                time.sleep(1)
                if Sec == 60:
                    Sec = 0
                    Min += 1
                    print(str(Min) + " Minute")

                if Min == 2:
                    sus_index +=1
                    print("Alert")
                    if Check == 1:
                        print("Suspicious activity detected inside ATM.")
                        Check += 1   

            if len(faces) > 2 and Counter == 1:
                print("Suspicious activity detected inside ATM.")
                Counter += 1
                sus_index +=1

                        
            if len(faces) == 0:

                print('No face detected')
                cv2.putText(img, "No face detected ", (0,img.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,255), 1)        
                Sec = 0
                Min = 0

            # cv2.imshow('img',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break  
            # img = buffer.tobytes()
            # yield (b'--frame\r\n'
            #     b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  

    cap.release()
    cv2.destroyAllWindows()
def moodDetection():
    face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    classifier =load_model(r'model.h5')

    emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            labels = []
            label = 'a'
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)

                    prediction = classifier.predict(roi)[0]
                    label=emotion_labels[prediction.argmax()]
                    label_position = (x,y)
                    cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    print(label)
                else:
                    cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            frame = buffer.tobytes()    
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def cctvframes():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def atmframes():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/mood')
def moodfeed():
    return Response(analysis(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/cctv')
def cctvfeed():
    return Response(cctvframes(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/atmcam')
def atmfeed():
    return Response(atmframes(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == "__main__":
    app.run()