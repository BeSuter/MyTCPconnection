import cv2
import json
import time
import socket

import numpy as np
import matplotlib.pyplot as plt


def recv(server):
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    pixel_count_str = ''
    char = server.recv(1)
    while char != b'\n':
        length_str += char.decode('utf-8')
        if length_str == b'Bye!!!!':
            print("The server said bye... :/ ")
            break
        char = server.recv(1)
    char = server.recv(1)
    while char != b'\n':
        pixel_count_str += char.decode('utf-8')
        char = server.recv(1)
    total = int(length_str)
    pixel_count = int(pixel_count_str)
    print("Total is: ", total)
    print("Number of pixels is. ", pixel_count)
    # use a memoryview to receive the data chunk by chunk efficiently
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = server.recv_into(view[next_offset:], total - next_offset)
        next_offset += recv_size
    try:
        deserialized = json.loads(view.tobytes())['data']
        deserialized = np.asarray(deserialized).reshape(pixel_count, 3)
    except (TypeError, ValueError):
        raise Exception('Data received was not in JSON format')
    return deserialized


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.5.177.178', 50000)
print(f"connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)
count = 0
all_times = []

try:
    while count < 1:
        # Send data
        s_time = time.time()
        print("Sending a message...")
        message = b'25.2\n'
        print(f"sending {message.decode('utf-8')}")
        sock.sendall(message)

        data = recv(sock)
        print("Received data has shape: ")
        print(np.shape(data))
        print(data)
        # Current data has shape [[xPos, yPos, temp],....[xPos, yPos, temp]] for all pixels with temp > tem_critical
        # Currently the data format is not compatible with the code below...
        """data = np.asarray(data)
        print("Maximum Temperature is ", np.max(data), " C. Minimum Temperature is ", np.min(data), " C.")
        tt = time.time() - s_time
        print(f"Time passed until received: {tt} seconds.")
        all_times.append(tt)
        plt.figure()
        plt.imshow(data, interpolation='none')
        plt.title("Full Thermal Image")
        plt.colorbar()
        plt.show()
    
        data = cv2.GaussianBlur(data, (3, 3), 0)
        laplacien = cv2.Laplacian(data, cv2.CV_64F, ksize=3)
        plt.figure()
        plt.imshow(laplacien, interpolation='none')
        plt.title("Laplacien Image")
        plt.colorbar()
        plt.show()"""
        count += 1
        print("")

        """# Look for the response
        amount_received = 0
        amount_expected = len("pong")
    
        while amount_received < amount_expected:
            data = sock.recv(16).decode('utf-16')
            amount_received += len(data)
            print(f"received {data}")"""

finally:
    print("closing socket")
    sock.close()

# print(f"Average time is {sum(all_times)/len(all_times)} seconds")
