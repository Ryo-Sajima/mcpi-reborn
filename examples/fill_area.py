import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('fill_area')


def main():
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    if not pos:
        print('player not found')
        return
    x, y, z = pos
    # fill a 3x3x3 cube centered on player feet level
    x0, y0, z0 = x-1, y, z-1
    x1, y1, z1 = x+1, y+2, z+1
    logger.info('filling area %s..%s with stone', (x0,y0,z0), (x1,y1,z1))
    mc.setBlocks(x0, y0, z0, x1, y1, z1, 'minecraft:stone')
    print('fill done')


if __name__ == '__main__':
    main()
