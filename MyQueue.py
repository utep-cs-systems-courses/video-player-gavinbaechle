from threading import *

class MyQueue:

    def __init__(self):

        self.queue = [] #the queue
        self.semaFull = Semaphore(0) #starts at zero because zero spots are available
        self.semaEmpty = Semaphore(10) #starts at 10 because 10 spots are available


    #put() adds a frame to the end of the queue
    #takes a frame as a parameter to add to the
    #end of the queue
    def put(self, frame):

        self.semaEmpty.acquire() #decrements empty (taking an available spot away)
        self.queue.append(frame) #add the frame to the queue
        self.semaFull.release() #increment full (filling a spot)

        
    #get() returns a frame from the front of the queue
    def get(self): 

        self.semaFull.acquire() #decrement from full (removing a spot from full)
        frame = self.queue.pop(0) #pops from the front of the queue
        self.semaEmpty.release() #increment empty (an empty spot just opened up)

        return frame
