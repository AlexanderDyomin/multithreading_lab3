import redis 

if __name__ == "__main__":
    conn = redis.Redis('localhost')
    # to prevent app start before Redis is up
    while 1:
        try:
            # print("trying to connect")
            conn.ping()
            print("It's finally over")
            break
        except redis.ConnectionError:
            continue
