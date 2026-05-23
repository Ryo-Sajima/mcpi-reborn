import sys
import os
import logging
import time
import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('integration_test')


def run():
    mc = Minecraft.create()
    out = {}
    # post chat
    try:
        mc.postToChat('integration test: hello')
        out['postToChat'] = 'ok'
    except Exception as e:
        out['postToChat'] = f'error: {e}'

    time.sleep(0.5)
    out['events'] = mc.events.pollChatPosts()

    # player info
    out['player_pos'] = mc.player.getPos()
    out['player_tile'] = mc.player.getTilePos()
    out['rotation'] = mc.player.getRotation()
    out['direction'] = mc.player.getDirection()

    # set a block above player and read it back
    px, py, pz = out['player_tile']
    mc.setBlock(px, py+1, pz, 'minecraft:stone')
    out['block_at'] = str(mc.getBlock(px, py+1, pz))

    # fill small area
    mc.setBlocks(px-1, py, pz-1, px+1, py+2, pz+1, 'minecraft:glass')

    # height
    out['height'] = mc.getHeight(px, pz)

    pprint.pprint(out)

if __name__ == '__main__':
    run()
