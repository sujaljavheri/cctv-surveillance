import cv2
import pickle
import numpy as np
import os
video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

if os.path.exists("data/names.pkl"):
    os.remove("data/names.pkl")

if os.path.exists("data/faces_data.pkl"):
    os.remove("data/faces_data.pkl")

faces_data=[]

i=0

name=input("Enter Your Name: ")

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    # Detect faces in the frame
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    #1.3 is threshold value, 5 is minimum neighbour
    # faces is a list of tuples (x, y, width, height) for each detected face
    # this for loop is used for rectangele frame
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :] # Crop the face from the frame
        # Resize the cropped image to 50x50 pixels
        resized_img=cv2.resize(crop_img, (50,50))
        if len(faces_data) < 30 and i%5==0:
            faces_data.append(resized_img)
        i=i+1
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)
    if k==ord('q') or len(faces_data)==30:
        break
video.release()
cv2.destroyAllWindows()

# faces_data=np.asarray(faces_data)
# faces_data=faces_data.reshape(100, -1)
faces_data = np.array(faces_data)
faces_data = faces_data.reshape(len(faces_data), -1)  # auto-calculate number of samples



if 'names.pkl' not in os.listdir('data/'):
    names=[name]*30
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names=pickle.load(f)
    names=names+[name]*30
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces=pickle.load(f)
    faces=np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)
