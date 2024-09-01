import cv2
import pickle
import numpy as np
import os

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eyedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

faces_data = []
i = 0

name = input("Enter Your Name: ")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        
        if len(faces_data) < 30 and i % 10 == 0:
            faces_data.append(resized_img)
        
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
        
        # Detect eyes within the detected face region
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eyedetect.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 1)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) >= 30:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(faces_data.shape[0], -1)

# Save names
names_file = 'data/names.pkl'
if not os.path.isfile(names_file):
    names = [name] * 30
else:
    with open(names_file, 'rb') as f:
        names = pickle.load(f)
    names += [name] * 30

with open(names_file, 'wb') as f:
    pickle.dump(names, f)

# Save faces data
faces_data_file = 'data/faces_data.pkl'
if not os.path.isfile(faces_data_file):
    with open(faces_data_file, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open(faces_data_file, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open(faces_data_file, 'wb') as f:
        pickle.dump(faces, f)
