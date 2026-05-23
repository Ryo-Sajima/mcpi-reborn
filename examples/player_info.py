import sys
import os
import logging
import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('player_info')


def main():
    mc = Minecraft.create()
    pos = mc.player.getPos()
    tile = mc.player.getTilePos()
    rot = mc.player.getRotation()
    pitch = mc.player.getPitch()
    direction = mc.player.getDirection()
    pprint.pprint({
        'pos': pos,
        'tile': tile,
        'rotation': rot,
        'pitch': pitch,
        'direction': direction,
    })


if __name__ == '__main__':
    main()
