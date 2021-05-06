#! /usr/bin/env python3


from functions import get_config as gc
from functions import extract_frames as ef
from functions import convert_to_grayscale as gs
from functions import display_frames as df
from functions import custom_queue as cq
from os import write
import sys
import os
import threading
import queue


if __name__ == '__main__':
    print("Starting Video Player.....")
    print("Reading configuration file...")

    config = gc.get_config()
    print("Configuration file successfully read")

    # inialize variables from config file
    buffer_size = config["bufferSettings"]["size"]

    # initialize queue
    work_queue = cq.CustomQueue()
    converted_queue = cq.CustomQueue()

    # initialize thread counters
    producer_thread_counter = 1
    consumer_thread_counter = 1

    # while 1:
    print("Starting Frame Producer Thread")
    thread_name = "Producer-thread-{}".format(producer_thread_counter)
    frame_producer_thread = ef.FrameProducerThread(
        producer_thread_counter, thread_name, work_queue)
    frame_producer_thread.start()

    print("Starting Frame Consumer Thread")
    thread_name = "Frame-consumer-thread-{}".format(consumer_thread_counter)
    frame_consumer_thread = gs.FrameConsumerThread(
        producer_thread_counter, thread_name, work_queue, converted_queue)
    frame_consumer_thread.start()

    print("Starting grayscale Frame Consumer Thread")
    thread_name = "Grayscale-Frame-consumer-thread-{}".format(
        consumer_thread_counter)
    grayscale_frame_consumer_thread = df.GrayscaleFrameConsumerThread(
        producer_thread_counter, thread_name, converted_queue)
    grayscale_frame_consumer_thread.start()

    # wait for the queue to empty
    # while not work_queue.empty():
    #    pass

    # Wait for all threads to complete
    # for thread in in_transfer_threads:
    #    thread.join()

    print("all threads completed!")

    # process_message(in_transfer_threads,conn,addr)
