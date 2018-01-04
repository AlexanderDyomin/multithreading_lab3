from flask import Flask
import redis 
import zmq
app = Flask(__name__)

conn = redis.Redis('redis')
if(int(conn.llen("fib")) == 0):
    conn.rpush("fib", 2 ,1)

@app.route('/')
def index():
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://worker:5555")
	#conn = redis.Redis('redis')
	x1 = conn.lindex("fib", 0)
	fib1 = int(x1)
	m = "Current Fibonacci num  = " + str(x1)
	socket.send('1')
	curFib = socket.recv()
	conn.lset("fib", 0, curFib)
	conn.lset("fib", 1, fib1)
	return m

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
