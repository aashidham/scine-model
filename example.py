from concurrence.io import BufferedStream, Socket
from concurrence import dispatch, Tasklet
from time import sleep
import pickle
import email_send2

import platform
platform.install()
import the_platform

import from_csv
import stitch


def handler(client_socket):
	r = BufferedStream(client_socket).reader
	f = r.file()
	text = f.read()
	[sid,email,params] = pickle.loads(text)
    
	platform.Platform.set_root("/home/cloud/scine-model/"+str(sid))
	f = open(str(sid)+"/"+str(sid)+".csv","wb")
	f.write(params)
	f.close()
	from_csv.run(str(sid)+"/"+str(sid)+".csv")
	email_send2.send_mail(email,str(sid),str(sid))

    

def start():
	server_socket = Socket.new()
	server_socket.bind(('localhost', 8080))
	server_socket.listen()
	
	while True:
		client_socket = server_socket.accept()
		Tasklet.new(handler)(client_socket)

if __name__ == '__main__':
    dispatch(start)