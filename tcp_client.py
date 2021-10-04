import cv2
import json
import socket

import numpy as np
import matplotlib.pyplot as plt


def recv(server):
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    char = server.recv(1)
    while char != b'\n':
        length_str += char.decode('utf-8')
        if length_str == b'Bye!!!!':
            print("The server said bye... :/ ")
            break
        char = server.recv(1)
    total = int(length_str)
    print("Total is: ", total)
    # use a memoryview to receive the data chunk by chunk efficiently
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = server.recv_into(view[next_offset:], total - next_offset)
        next_offset += recv_size
    try:
        deserialized = json.loads(view.tobytes())
    except (TypeError, ValueError):
        raise Exception('Data received was not in JSON format')
    return deserialized


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('10.5.177.178', 50000)
print(f"connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

try:
    # Send data
    print("Sending a message...")
    message = b'ping'
    print(f"sending {message.decode('utf-8')}")
    sock.sendall(message)

    data = recv(sock)
    print("Received data has shape: ")
    print(np.shape(data))
    data = np.asarray(data)
    print("Maximum Temperature is ", np.max(data), " C. Minimum Temperature is ", np.min(data), " C.")
    plt.figure()
    plt.imshow(data, interpolation='none')
    plt.show()

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
