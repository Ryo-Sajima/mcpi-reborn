import sys
import os
import logging
import time

# ensure package path: add ../ (python/) to sys.path so `mcpi` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('hello_post')


def main():
    mc = Minecraft.create()
    msg = "hello from Python"
    logger.info("sending message: %s", msg)
    try:
        mc.postToChat(msg)
        logger.info("message sent")
        print('sent')
    except Exception as e:
        logger.exception("failed to send message")
        print('error:', e)


if __name__ == '__main__':
    main()
