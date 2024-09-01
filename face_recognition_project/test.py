import cv2
import numpy as np
import os
import csv
import time
from datetime import datetime
import pickle
from sklearn.neighbors import KNeighborsClassifier
import pyttsx3

class UnrecognizedFaceException(Exception):
    """Exception raised for unrecognized faces."""
    def __init__(self, message="Face not recognized from faces_data.pkl"):
        self.message = message
        super().__init__(self.message)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def load_resources():
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        raise Exception("Could not open video device")

    facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    if facedetect.empty():
        raise Exception("Could not load face detection model")

    with open('data/names.pkl', 'rb') as w:
        LABELS = pickle.load(w)
    with open('data/faces_data.pkl', 'rb') as f:
        FACES = pickle.load(f)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)

    imgBackground = cv2.imread("background.png")
    if imgBackground is None:
        raise Exception("Background image not found")

    return video, facedetect, knn, imgBackground, LABELS

def process_frame(frame, facedetect, knn, trained_labels):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    recognized_name = None
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        recognized_name = output[0]
        
        if recognized_name in trained_labels:
            frame = annotate_frame(frame, x, y, w, h, recognized_name, color=(255, 255, 255))
        else:
            frame = annotate_frame(frame, x, y, w, h, "Unrecognized", color=(0, 0, 255))
            raise UnrecognizedFaceException()

    return frame, recognized_name, len(faces)

def annotate_frame(frame, x, y, w, h, name, color=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    if name:
        cv2.rectangle(frame, (x, y-30), (x+w, y), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (x + 6, y - 6), font, 1, color, 2)
        
    return frame

def handle_attendance(name, index_number, program, course_title):
    date = datetime.now().strftime("%d-%m-%Y")
    timestamp = datetime.now().strftime("%H:%M:%S")
    attendance = [name, index_number, program, course_title, timestamp]
    file_path = f"Attendance/Attendance_{date}.csv"
    
    if os.path.isfile(file_path):
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            existing_records = list(reader)
    else:
        existing_records = []

    if not any(row[0] == name and row[1] == index_number for row in existing_records):
        try:
            with open(file_path, "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not existing_records:
                    COL_NAMES = ['NAME', 'INDEX', 'PROGRAM', 'COURSE TITLE', 'TIME']
                    writer.writerow(COL_NAMES)
                writer.writerow(attendance)
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

def flash_green(frame, imgBackground):
    green_flash = np.zeros_like(frame)
    green_flash[:] = (0, 255, 0)
    imgBackground[162:162 + 480, 55:55 + 640] = green_flash
    cv2.imshow("Frame", imgBackground)
    cv2.waitKey(500)

def show_no_faces_message(frame, imgBackground):
    message = "No faces detected"
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(message, font, 2, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = frame.shape[0] // 2
    cv2.putText(frame, message, (text_x, text_y), font, 2, (0, 0, 255), 2)
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    cv2.waitKey(2000)

def draw_hud(frame, facedetect):
    border_color = (0, 255, 0)
    thickness = 2
    cv2.rectangle(frame, (50, 50), (frame.shape[1] - 50, frame.shape[0] - 50), border_color, thickness)

    font = cv2.FONT_HERSHEY_SIMPLEX
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    cv2.putText(frame, current_time, (60, 40), font, 1, (255, 255, 255), 2)

    progress_bar_length = 200
    progress = int((time.time() % 10) * 20)
    cv2.rectangle(frame, (60, frame.shape[0] - 40), (60 + progress, frame.shape[0] - 20), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(frame, (60, frame.shape[0] - 40), (60 + progress_bar_length, frame.shape[0] - 20), (255, 255, 255), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    face_status = "Faces Detected" if len(faces) > 0 else "No Faces"
    text_size = cv2.getTextSize(face_status, font, 1.5, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    cv2.putText(frame, face_status, (text_x, frame.shape[0] - 60), font, 1.5, (0, 255, 255), 2)

def display_current_index_on_frame(frame, current_index_number):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Current Index: {current_index_number}"
    # Reduced font scale for smaller text
    cv2.putText(frame, text, (10, 70), font, 0.7, (255, 255, 255), 2)

def main():
    program = input("Enter your program: ").strip()
    course_title = input("Enter the course title: ").strip()
    num_pupils = int(input("Enter the number of pupils: ").strip())
    index_numbers = []

    for i in range(num_pupils):
        index_number = input(f"Enter index number for pupil {i+1}: ").strip()
        index_numbers.append(index_number)

    try:
        video, facedetect, knn, imgBackground, trained_labels = load_resources()
    except Exception as e:
        print(f"Error loading resources: {e}")
        return

    last_face_detection_time = time.time()
    inactivity_threshold = 10
    current_pupil_index = 0

    while current_pupil_index < num_pupils:
        ret, frame = video.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Apply mirror effect
        frame = cv2.flip(frame, 1)

        current_index_number = index_numbers[current_pupil_index]
        display_current_index_on_frame(frame, current_index_number)

        try:
            frame, recognized_name, num_faces = process_frame(frame, facedetect, knn, trained_labels)
        except UnrecognizedFaceException as e:
            print(e)
            speak(str(e))
            show_no_faces_message(frame, imgBackground)
            continue

        if num_faces > 0:
            last_face_detection_time = time.time()

        draw_hud(frame, facedetect)

        if time.time() - last_face_detection_time >= inactivity_threshold:
            show_no_faces_message(frame, imgBackground)

        imgBackground[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow("Frame", imgBackground)

        k = cv2.waitKey(1)
        if k == ord('o') or k == ord('O'):
            if recognized_name:
                message = f"Attendance Taken for {recognized_name} (Index: {current_index_number})"
                speak(message)
                cv2.putText(frame, message, (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Frame", frame)
                cv2.waitKey(2000)

                handle_attendance(recognized_name, current_index_number, program, course_title)

                flash_green(frame, imgBackground)

                # Move to the next pupil
                current_pupil_index += 1

        elif k == ord('q') or k == ord('Q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
