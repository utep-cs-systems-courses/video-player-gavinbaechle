#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from queueClass import queueClass

def extractFrames(fileName, extractionFrames, maxFramesToLoad=9999):
    # Initialize frame count
    count = 0
    # open video file
    vidcap = cv2.VideoCapture(fileName)
    # read first image
    success,image = vidcap.read()

    print('Reading frame: ' , count, ' ', success)
    while success and count < maxFramesToLoad:
        # add the frame to the buffer
        extractionFrames.put(image)
        success,image = vidcap.read()
        print('Reading frame: ' , count, ' ', success)
        count += 1

    print('Frame extraction complete')
    extractionFrames.markEnd()

def convertToGrayScale(extractionFrames, conversionFrames):
    count = 0
    while True and count < 72:
        print('Converting frame: ', count)
        frame = extractionFrames.get() #attain the frames
        if frame == 'end':
            #if we see the mark
            break #exit the loop

        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY ) #frame to grey
        conversionFrames.put(greyFrame) #put in the queue
        count += 1 #increment

    print('Frame Conversion complete')
    conversionFrames.markEnd()

def displayFrames(inputBuf):
    count = 0
    while True:
        frame = inputBuf.get() #get a frame
        if frame == 'end':
            break #end the while

        print('Displaying frame: ', count)
        cv2.imshow('Video', frame) #show the frame image
        if cv2.waitKey(42) and 0xFF == ord('q'): #wait for 42 ms
            break
        count += 1

    print('Finished Displaying')
    cv2.destroyAllWindows()

file_name = 'clip.mp4'
extractionQueue = queueClass()
conversionQueue = queueClass()

#extract and convert
extractThread = threading.Thread(target = extractFrames, args = (file_name, extractionQueue, 72)) #threading for extraction frames
conversionThread = threading.Thread(target = convertToGrayScale, args = (extractionQueue, conversionQueue)) #threading to convert the extracted frames

#display the converted frames
displayThread = threading.Thread(target = displayFrames, args = (conversionQueue,)) #threading to display frames

#begin the thread
extractThread.start()
conversionThread.start()
displayThread.start()
