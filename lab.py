import cv2
import numpy as np

from threading import Thread
from MyQueue import *


#extractFrames breaks down the video into frames
#and puts the frames into the queue that stores the
#colored images.
def extractFrames(fileName, colorQueue, maxFrames):

    count = 0
    videoCap = cv2.VideoCapture(fileName)
    success, image = videoCap.read() #gets the first image

    while success and count < maxFrames:

        colorQueue.put(image) #puts image in the queue
        count += 1
        success, image = videoCap.read() #refreshes to get the rest of the images

    colorQueue.put(None) #None indicates the end of the file is reached


#convertToGray converts the frames in the queue
#containing the colored frames to gray frames
def convertToGray(colorInput, grayOutput):

    count = 0
    currentFrame = colorInput.get() #gets the first frame

    while (currentFrame is not None):

        grayFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY) #converts currentFrame to gray
        grayOutput.put(grayFrame) #puts the gray frame into another queue storing the gray frames
        count += 1

        currentFrame = colorInput.get() #refresh currentFrame to get the rest of the images

    grayOutput.put(None) #reached the end of the video
    
    
#displayFrames takes a queue containing frames and
#displays the images
def displayFrames(inputQueue):

    count = 0
    currentFrame = inputQueue.get() #gets the first frame

    while currentFrame is not None:

        cv2.imshow('Video', currentFrame)

        if(cv2.waitKey(42) and 0xFF == ord("q")):
            break

        count += 1
        currentFrame = inputQueue.get() #refresh the current frame

    cv2.destroyAllWindows()



def main():
    
    maxFrames = 72
    colorQueue = MyQueue() 
    grayQueue = MyQueue() 
    videoCapture = cv2.VideoCapture("clip.mp4")

    threadList = [Thread(target = extractFrames, args = ["clip.mp4", colorQueue, maxFrames]),
                  Thread(target = convertToGray, args = [colorQueue, grayQueue]),
                  Thread(target = displayFrames, args = [grayQueue])]

    for i in threadList:
        i.start()
    
    for i in threadList:
        i.join()
    


if __name__== "__main__":
    main()
