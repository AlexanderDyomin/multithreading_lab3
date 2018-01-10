import redis
import zmq

def fib(conn):
    pipe = conn.pipeline()
    while 1:
        try:
            pipe.watch("fib")
            x2 = pipe.lindex("fib", 1)
            x1 = pipe.lindex("fib", 0)
            fib1 = int(x1)
            fib2 = int(x2)
            curFib = fib1 + fib2
            pipe.multi()
            pipe.lset("fib", 0, curFib)
            pipe.lset("fib", 1, fib1)
            pipe.execute()
            break
            #strCurFib = str(curFib)
            #return strCurFib
        except redis.WatchError:
            continue
        finally:
            pipe.reset()
    return
            
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
conn = redis.Redis('redis')
while True:
    mes = socket.recv() # recieved dumb message, time to work
    fib(conn)
    socket.send('done')
