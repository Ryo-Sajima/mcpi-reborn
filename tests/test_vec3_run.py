from python.mcpi.vec3 import Vec3

t = Vec3(10, 64, 10)
print("tile:", t, tuple(t), type(next(iter(t))))

p = Vec3(10.5, 64.0, 10.0)
print("pos:", p, tuple(p), type(next(iter(p))))

def demo_setblock(x: int, y: int, z: int, block: str):
    print("setBlock called with", x, y, z, block)

# Unpack integer Vec3 into setBlock
demo_setblock(*t, "minecraft:grass_block")

# Arithmetic mixes to floats
print("t + p ->", t + p)
