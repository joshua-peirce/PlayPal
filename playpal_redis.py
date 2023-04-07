"""
playpal redis
"""

# import statements
import redis
import uuid
import time


class PlayPI:
    """ API simulating basic Twitter """

    def __init__(self, channel, host='localhost', port=6379, db=0):
        """ initialize connection and flush any previous connection """
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.channel = channel

    def flush_all(self):
        self.r.flushall()

    def insert_one_user(self, user_id, pw, rating, skill_level):
        self.r.sadd(f'users:{user_id}', pw, rating, skill_level)

    def insert_all_users(self, users):
        """ insert all users """
        pipe = self.r.pipeline()
        for user_id, pw, rating, skill_level in users:
            pipe.sadd(f'users:{user_id}', pw, rating, skill_level)
        pipe.execute()

    def insert_one_game(self, game_id, p1, p2, ):

    def get_followers(self, user_id):
        """ gets who is following a particular user """
        followers = self.r.smembers(f"follows:{user_id}")
        return followers

    def post_tweet(self, user_id, text):
        """
        posts single tweet
        where the key is the tweet ID (perhaps “Tweet:12345”)
        and the value is the contents of the tweet
        """

        # generate random tweet_id
        tweet_id = str(uuid.uuid4())
        # generate timestamp at time of insert
        timestamp = time.time() * 1000

        # post the tweet
        self.r.hmset(f"tweet:{tweet_id}", {"user_id": user_id,
                                           "timestamp": timestamp,
                                           "text": text})

    def post_tweet_timelines(self, user_id, text):
        """ posts single tweet and updates the followers timelines """

        # generate random tweet_id
        tweet_id = str(uuid.uuid4())
        # generate timestamp at time of insert
        timestamp = time.time() * 1000

        # post the tweet
        self.r.hmset(f"tweet:{tweet_id}", {"user_id": user_id,
                                           "timestamp": timestamp,
                                           "text": text})

        # get all followers for the user
        followers = self.get_followers(user_id)
        pipeline = self.r.pipeline()

        # add the tweet to each of the user's followers' timelines
        for follower in followers:
            pipeline.lpush(f"timeline:{follower}", tweet_id)

        pipeline.execute()

    def make_and_get_timeline(self, user_id):
        """
        gets the 10 most recent tweets
        from everyone user_id follows
        """

        # get followers
        followers = self.get_followers(user_id)

        tweets = []
        # add tweets from each follower to timeline
        for follower in followers:
            follower_tweets = self.user_tweets(follower)
            # Add the tweets to the list
            tweets.extend(follower_tweets)

        # sort by timestamp in desc order
        sorted_tweets = sorted(tweets, key=lambda x: float(x['timestamp']), reverse=True)
        # return 10 most recent tweets
        return sorted_tweets[:10]

    def get_timeline(self, user_id):
        """ gets 10 most recent tweets from particular user """

        # gets tweet_ids from timeline
        timeline = self.r.lrange(f"timeline:{user_id}", 0, 9)

        # gets tweet info (user_id, text, and timestamp) for each timeline tweet
        tweet_info = []
        for tweet_id in timeline:
            tweet = self.r.hgetall(f"tweet:{tweet_id}")
            tweet_info.append(tweet)
        # sort 10 most recent tweets for timeline
        tweet_info = sorted(tweet_info, key=lambda x: x["timestamp"], reverse=True)
        return tweet_info[:10]

    def user_tweets(self, user_id):
        """ gets all the tweets tweeted by one user """
        tweets = []
        for tweet_id in self.r.scan_iter(match=f"tweet:*"):
            tweet = self.r.hgetall(tweet_id)
            if tweet["user_id"] == str(user_id):
                tweets.append(tweet)
        return tweets

    def get_unique_users(self, df):
        """ gets unique user_ids from a df """
        unique_user_ids = df['USER_ID'].drop_duplicates().tolist()
        return unique_user_ids
