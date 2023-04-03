"""
Date: 4/2/23

"""

import redis
import player
redis_host = 'localhost'
redis_port = 6379

rc = redis.Redis(host=redis_host, port=redis_port)

def start_client(id):
    ps = rc.pubsub()
    ps.subscribe("game")
    rc.publish("game", f"join:{id}")
    player.ClientSidePlayer(rc, ps, id==0)

if __name__ == "__main__":
    start_client(int(input("client id: ")))

    """
import redis

def main():
    r = redis.Redis('localhost', 6379, decode_responses=True)
    sub = r.pubsub()
    sub.subscribe('jobs')
    while True:
        for message in sub.listen():
            if message['type'] == 'message':
                data = message['data']
                vals = [int(x) for x in data.split(',')]
                id, user, x, y = vals
                answer = x + y
                print(x, y, answer)
                r.lpush(f'timeline:{user}',
                        f"answer for job {id} is {answer}")


main()"""