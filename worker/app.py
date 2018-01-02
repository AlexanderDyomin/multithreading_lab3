import redis
import zmq 

def fib():
	conn = redis.Redis('redis')
	x2 = conn.lindex("fib", 1)
	x1 = conn.lindex("fib", 0)
	fib1 = int(x1)
	fib2 = int(x2)
	curFib = fib1 + fib2
	strCurFib = str(curFib)
	return strCurFib

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
while True:
	mes = socket.recv()
	curFib = fib()
	socket.send(curFib)
