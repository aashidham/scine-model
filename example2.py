import socket,pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = sock.connect(('localhost', 8080))
sock.sendall(pickle.dumps(['a','b','c']))