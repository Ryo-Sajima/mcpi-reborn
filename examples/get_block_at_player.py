import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('get_block_at_player')


def main():
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    if not pos:
        print('player not found')
        return
    x, y, z = pos
    blk = mc.getBlock(x, y-1, z)
    print('block at player:', blk)


if __name__ == '__main__':
    main()
