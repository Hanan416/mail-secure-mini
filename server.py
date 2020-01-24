import socket
import pysftp

sock = socket.socket()
host = socket.gethostname()
port = 8080
sock.bind((host, port))
sock.listen(1)
print("Hosting on ", host)
print("Server socket is up, Waiting for connections... ")
conn, addr = sock.accept()
print(addr, " is connected to the server")