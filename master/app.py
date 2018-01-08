from flask import Flask
import redis 
import zmq
app = Flask(__name__)

@app.route('/')
def index():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://worker:5555")
    #conn = redis.Redis('redis')
    x1 = conn.lindex("fib", 0)
    fib1 = int(x1)
    m = "Current Fibonacci num  = " + str(x1)
    socket.send('next') # dumb message just to send to worker and make it work
    answer = socket.recv()
    #conn.lset("fib", 0, curFib)
    #conn.lset("fib", 1, fib1)
    return m

if __name__ == "__main__":
    conn = redis.Redis('redis')
    # to prevent app start before Redis is up
    while 1:
        try:
            # print("trying to connect")
            conn.ping()
            break
        except redis.ConnectionError:
            continue
    
    if(int(conn.llen("fib")) == 0):
        conn.rpush("fib", 2 ,1)

    app.run(host="0.0.0.0", debug=True)
