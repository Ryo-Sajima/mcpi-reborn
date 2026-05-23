import sys
import os
import logging
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('poll_chat')


def main():
    mc = Minecraft.create()
    # post a message then poll
    mc.postToChat('python poll_chat test')
    time.sleep(0.5)
    events = mc.events.pollChatPosts()
    print('events:', events)


if __name__ == '__main__':
    main()
