# Driver file
import game
from board import Board
from client import Client
from player import Player
import redis
import subprocess
from server import Server

# Start the redis-cli in a subprocess
redis_cli_process = subprocess.Popen(["redis-cli"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

# Connect to Redis using RedisPy
r = redis.Redis()

# Define a function to send commands to redis-cli
def send_command_to_redis_cli(command):
    redis_cli_process.stdin.write(command + "\n")
    redis_cli_process.stdin.flush()
    output = redis_cli_process.stdout.readline().strip()
    return output

# Autoincremented ID
auto_increment_id = 0

while True:
    # Send message to Redis
    message = input("Enter a message to send to Redis (or 'quit' to exit): ")
    if message.lower() == 'quit':
        break
    r.set(f"message:{auto_increment_id}", message)
    print(f"Sent message with ID: {auto_increment_id}")
    auto_increment_id += 1

    # Get messages from Redis
    messages = send_command_to_redis_cli("LRANGE messages 0 -1")
    print("Messages from Redis:")
    for idx, msg in enumerate(messages):
        print(f"{idx+1}. {msg}")


