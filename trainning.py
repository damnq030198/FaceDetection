import cv2
import os
import numpy as np
from PIL import Image
import sqlite3
import dataSet


def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg,'uint8')
        #split to get ID of the image
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(ID)
        IDs.append(ID)
        cv2.imshow("traning",faceNp)
        cv2.waitKey(100)
    return IDs, faces

def getAllId():
    con = dataSet.sql_connection()
    cmd= "SELECT * FROM People"
    cursor=con.execute(cmd)
    profile = []
    for row in cursor:
        profile.append(row[0])
    return profile

def traindata():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    ids = getAllId()
    for id in ids:
        path='dataSet/'+str(id)
        Ids,faces=getImagesAndLabels(path)
    #trainning
    recognizer.train(faces,np.array(Ids))
    recognizer.save('recognizer/trainningData.yml')
    cv2.destroyAllWindows()
