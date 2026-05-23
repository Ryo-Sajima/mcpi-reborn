import sys
import os
import logging
import time

# ensure python/ is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('set_block_at_player')


def main():
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    if not pos:
        print('player not found')
        return
    x, y, z = pos
    logger.info('setting block at %s,%s,%s', x, y, z)
    try:
        mc.setBlock(x, y, z, 26)
        print('setBlock done')
    except Exception as e:
        logger.exception('failed setBlock: %s', e)


if __name__ == '__main__':
    main()
