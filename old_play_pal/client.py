"""
Date: 4/2/23

"""

import redis
import player
redis_host = 'localhost'
redis_port = 6379


class Client:
    pass

rc = redis.Redis(host=redis_host, port=redis_port)


def start_client():
    ps = rc.pubsub()

    last_id = rc.llen('player_ids')
    print(last_id)

    # sub to individual channel
    ps.subscribe(f"player{last_id}")
    # increase length of player list
    rc.lpush('player_ids', 0)

    # have them subscribe to game channel?
    rc.publish(f"player{last_id}", f"join:player{last_id}")
    player.ClientSidePlayer(rc, ps, id == 0)

if __name__ == "__main__":
    start_client()

    """
    FROM RACHLIN CODE
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
