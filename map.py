import random

class Tile:
    def __init__(self, char, color, name, blocked, block_sight=None):
        self.char = char
        self.color = color
        self.name = name
        self.blocked = blocked
        
        
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight


class Room:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(" ", "black", "adamant", True) for y in range(self.height)] for x in range(self.width)]

        # number of rooms
        rooms = random.randint(6,9)
        centerlist = []

        for z in range(rooms):
            #choose room center
            rx = random.randint(8, self.width - 8)
            ry = random.randint(8, self.height - 8)

            centerlist.append(Room(rx, ry))

            xsize = random.randint(1,5)
            ysize = random.randint(1,5)

            for x in range(rx - xsize, rx + xsize):
                for y in range(ry - ysize, ry + ysize):
                        #print(x)
                        #print(y)
                        if (0<x<self.width-1) and (0<y<self.height-1):
                            tiles[x][y].char = "."
                            tiles[x][y].color = "darker grey"
                            tiles[x][y].name = "room"
                            tiles[x][y].blocked = False
                            tiles[x][y].block_sight = False

            # make paths for each room

            for n in range(len(centerlist)-1):
                cx1 = centerlist[n].cx
                cy1 = centerlist[n].cy
                
                #choose another room
                m = n
                while m == n:
                    m = random.randint(0,len(centerlist)-1)

                cx2 = centerlist[m].cx
                cy2 = centerlist[m].cy

                if random.randint(1,1) == 1:
                    if cx2 > cx1:
                        xstep = 1
                    else:
                        xstep = -1
                    for pathx in range(cx1, cx2, xstep):
                        if tiles[pathx][cy1].name == "adamant":
                            tiles[pathx][cy1].char = "."
                            tiles[pathx][cy1].color = "lighter grey"
                            tiles[pathx][cy1].name = "horz hallway"
                            tiles[pathx][cy1].blocked = False
                            tiles[pathx][cy1].block_sight = False

                    if cy2 > cy1:
                        ystep = 1
                    else:
                        ystep = -1
                    for pathy in range(cy1, cy2, ystep):
                        if tiles[cx2][pathy].name == "adamant":
                            tiles[cx2][pathy].char = "."
                            tiles[cx2][pathy].color = "lighter grey"
                            tiles[cx2][pathy].name = "vert hallway"
                            tiles[cx2][pathy].blocked = False
                            tiles[cx2][pathy].block_sight = False
                else:
                    for pathy in range(min(cy1, cy2), max(cy1, cy2)):
                        tiles[cx1][pathy].blocked = False
                        tiles[cx2][pathy].block_sight = False

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False