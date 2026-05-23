import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python.mcpi.minecraft import Minecraft

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('get_height')


def main():
    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    if not pos:
        print('player not found')
        return
    x, _, z = pos
    h = mc.getHeight(x, z)
    print('height at', x, z, '->', h)


if __name__ == '__main__':
    main()
