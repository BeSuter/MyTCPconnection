import sys
import os

import json
import socket

import cv2

sys.path.insert(0, os.path.abspath("."))

from radiometry_test import *


def send(_client, _data):
    try:
        serialized = json.dumps(_data).encode('utf-8')
    except (TypeError, ValueError):
        raise Exception('You can only send JSON-serializable data')
    # send the length of the serialized data first
    header = b'%d\n' % len(serialized)
    _client.send(header)
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
        data = client.recv(size)
        if data == b'ping':
            print("Unity Sent: " + str(data.decode('utf-8')) + "sending back one Lepton frame")
            data = cam.get_frame()
            data = data.tolist()
            send(client, data)
            print("Sent one frame... ")
            # client.send("pong".encode('utf-16'))
        else:
            client.send(b'Bye!!!!')
            # print("Unity Sent Something Else: " + str(data.decode('utf-8')))
            # client.close()
            # break
