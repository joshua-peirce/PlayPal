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


main()
