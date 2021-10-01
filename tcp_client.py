import cv2
import json
import socket


def recv(server):
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    char = server.recv(1).decode('utf-16')
    while char != '\n':
        length_str += char
        if length_str == "Bye!!!!":
            print("The server said bye... :/ ")
            break
        char = server.recv(1).decode('utf-16')
    total = int(length_str)
    # use a memoryview to receive the data chunk by chunk efficiently
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = server.recv_into(view[next_offset:], total - next_offset).decode('utf-16')
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
    message = "ping"
    print(f"sending {message}")
    sock.sendall(message.encode('utf-16'))

    data = recv(sock)
    print("Received data was: ")
    print(data)

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
