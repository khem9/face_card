Facial Recognition Attendance System
This project uses facial recognition technology to record and manage attendance. It includes scripts for training a facial recognition model, testing and recording attendance, and viewing the attendance log through a local web application.

Scripts
add_faces.py
Description:

add_faces.py is used to train a facial recognition model using the Haar Cascade classifier. It detects faces, processes face data, and saves the trained model and associated data.

Dependencies:

cv2 (OpenCV)
pickle
numpy
os (standard library)
Install dependencies using:

bash
Copy code
pip install opencv-python-headless numpy
Functionality:

Detects faces using Haar Cascade.
Processes and collects face data for training.
Saves names and face data to names.pkl and faces_data.pkl.
Data Files:

names.pkl: Stores names associated with each detected face.
faces_data.pkl: Contains facial data used for training.
Usage:

Run the script:

bash
Copy code
python add_faces.py
test.py
Description:

test.py tests and detects faces using the trained model from add_faces.py. It records attendance with details like time, course title, program, and detected names, saving the data in an Excel file.

Dependencies:

cv2 (OpenCV)
numpy
os (standard library)
csv
time
datetime (standard library)
pickle
sklearn.neighbors (KNeighborsClassifier)
pyttsx3
Install dependencies using:

bash
Copy code
pip install opencv-python-headless numpy scikit-learn pyttsx3
Functionality:

Face Detection and Recognition: Detects and recognizes faces in real-time.
User Input: Collects inputs for program name, course title, number of pupils, and their index numbers.
Attendance Recording: Saves attendance with details in attendance_log.csv including date and time.
Audio Feedback: Provides audio feedback using pyttsx3.
Usage:

Run the script:

bash
Copy code
python test.py
Instructions:

Enter the program name.
Enter the course title.
Enter the number of pupils.
Input the index numbers for each pupil in the specified order.
app.py
Description:

app.py is a Streamlit application that displays the attendance log locally. It automatically refreshes every 2 seconds to show the latest data.

Dependencies:

streamlit
cv2 (OpenCV)
numpy
os (standard library)
csv
time
datetime (standard library)
pickle
sklearn.neighbors (KNeighborsClassifier)
pyttsx3
Install dependencies using:

bash
Copy code
pip install streamlit opencv-python-headless numpy scikit-learn pyttsx3
Functionality:

Local Hosting: Hosts the attendance log locally using Streamlit.
Automatic Refresh: Page refreshes every 2 seconds to display up-to-date attendance data.
Data Display: Shows contents of attendance_log.csv, including time, course title, program, and names.
Usage:

Run the Streamlit application:

bash
Copy code
streamlit run app.py
Open the provided local URL in a web browser to view the attendance log.

Notes
Ensure add_faces.py is run to train the model before using test.py.
Verify that names.pkl, faces_data.pkl, and attendance_log.csv are in the correct directory for both scripts.
Adjust paths and settings in the scripts as needed for your environment.
Attendance data is recorded in attendance_log.csv and includes date and time.
