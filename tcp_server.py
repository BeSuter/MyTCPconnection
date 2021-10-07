import sys
import os

import json
import socket

import cv2

sys.path.insert(0, os.path.abspath("."))

from radiometry_test import *


def send(_client, _data, _pixel_count):
    try:
        serialized = json.dumps(_data).encode('utf-8')
    except (TypeError, ValueError):
        raise Exception('You can only send JSON-serializable data')
    # send the length of the serialized data first
    header1 = b'%d\n' % len(serialized)
    header2 = b'%d\n' % _pixel_count
    print(f"First Header is {header1}")
    print(f"Second Header is {header2}")
    _client.send(header1)
    _client.send(header2)
    # send the serialized data
    _client.sendall(serialized)


"""class LeptonCam:
    def __init__(self, client):
        self.vid = cv2.VideoCapture(0)
        self.client = client

    def get_frame(self):
        _, frame = self.vid.read()
        serialized_frame = json.dumps(frame.tolist())
        print("Sending one video frame")
        header = '%d\n' % len(serialized_frame)
        client.sendall(header.encode('utf-16'))
        client.sendall(serialized_frame.encode('utf-16'))"""


host = '10.5.177.178'
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

while 1:
    print("Looking for a client...")
    client, address = s.accept()
    print(f"Client connected. Address is {address}")
    print("Starting Lepton camera")
    cam = LeptonCam()

    while 1:
        temp_str = ""
        char = client.recv(1)
        while char != b'\n':
            temp_str += char.decode('utf-8')
            char = client.recv(1)
        temperature = float(temp_str)
        if len(temp_str) > 0:
            print("Unity Sent: " + temp_str + " sending back one Lepton frame")
            pixel_count, data = cam.get_frame(temperature)
            data = data.tolist()
            send(client, data, pixel_count)
            print("Sent one frame... ")
            # client.send("pong".encode('utf-16'))
        else:
            client.send(b'Bye!!!!')
            # print("Unity Sent Something Else: " + str(data.decode('utf-8')))
            # client.close()
            # break
