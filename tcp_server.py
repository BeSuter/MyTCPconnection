import socket

host = '10.5.177.178'
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

while 1:
    print("Trying to connect...")
    client, address = s.accept()
    print(f"Client connected. Address is {address}")
    while 1:
        data = client.recv(size).decode('utf-16')
        if data == "ping":
            print("Unity Sent: " + str(data))
            client.send("pong".encode('utf-16'))
        else:
            client.send("Bye!!!!".encode('utf-16'))
            print("Unity Sent Something Else: " + str(data))
            # client.close()
            # break
