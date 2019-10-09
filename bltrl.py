from bearlibterminal import terminal as blt
import map
import math
import sys
import random
import os
import textwrap
from time import time

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, name, char, color):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.Health = 100
        self.LifeSupport = 50
        self.power = 0
        self.angst = 1

        self.atk = 10
        self.defense = 10
        
        self.LS_Rate = 1

        self.Ethereal = False

    # Attempt to move the entity by a given amount
    def move(self, dx, dy):
        #check other entities
        ent_blocks = False
        for ent in entities:
            if ent.x == self.x + dx and ent.y == self.y + dy:
                ent_blocks = True
                self.attack(ent)
                
        if not gamemap.is_blocked(self.x+dx, self.y+dy) and not ent_blocks:
            self.x += dx
            self.y += dy
            self.LifeSupport += self.LS_Rate

    def injure(self, injury):
        self.Health -= injury
        if self.name == player.name:
            message_log.add_message(Message("You are injured", "light red")) 

    def attack(self, entity):
        AttackRating = random.randrange(1, self.atk)
        DefenseRating = random.randrange(1, entity.defense)
        if AttackRating > DefenseRating:
            self.injure(AttackRating - DefenseRating)
            if self.name == player.name:
                message_log.add_message(Message("You attack the "+entity.name+" and do "+str(AttackRating-DefenseRating)+" damage", "red"))
        else:
            if self.name == player.name:
                message_log.add_message(Message("You attack the "+entity.name+" but miss", "dark red"))            
    


class Player(Entity):
    def __init__(self, x, y, name, char, color, CanSeeColor=False, CanSenseLayers=False):
        super().__init__(x, y, name, char, color)
        self.CanSeeColor = CanSeeColor
        self.CanSenseLayers = CanSenseLayers

    def ConsumeItemFromFloor(self):
        if len(items_present) > 0:
            for i in range(0, len(items) - 1):
                if items[i].x == player.x and items[i].y == player.y:
                    player.LifeSupport += items_present[0].nutra_value
                    player.angst += items_present[0].mutat_value
                    del items[i]
                    IncrementTurn = True
                    EatMessage = Message("You eat " + str.lower(items_present[0].name))
                    message_log.add_message(EatMessage)                    
                    break
            return IncrementTurn

    
class Item:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, name, char, color):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.nutra_value = 0
        self.mutat_value = 0

class Projectile:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, name, projtype, color):
        self.x = x
        self.y = y
        self.name = name
        self.projtype = projtype
        self.color = color

class Message:
    def __init__(self, text, color="white"):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            while len(self.messages) > self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))

blt.composition(True)

def render_all(entities, gamemap):
    #blt.clear()
    # Draw all the tiles in the game map
    blt.layer(0)
    blt.bkcolor("black")
    for y in range(gamemap.height):
        for x in range(gamemap.width):
            blt.puts(x, y, "[color=%s]%s[/color]" % (gamemap.tiles[x][y].color, gamemap.tiles[x][y].char))    

    blt.layer(100)
    # Draw all entities in the list
    for entity in entities:
        draw_entity(entity)

    # Draw all items on the list
    blt.layer(10)
    for i in items:
        draw_item(i)

    blt.layer(255)
    
    draw_UI()
    blt.layer(254)
    blt.puts(0, 49, "[color=lighter yellow]%s[/color]" % fps_value)
    DrawReticle()

    ### Draw animations

    blt.refresh()

def clear_all():
    for entity in entities:
        clear_entity(entity)

def draw_entity(entity):
    if player.CanSeeColor or entity.name == "Player":
        blt.puts(entity.x, entity.y, "[color=%s]%s[/color]" % (entity.color, entity.char))
    else:
        blt.puts(entity.x, entity.y, "[color=%s]%s[/color]" % ("grey", entity.char))

def draw_item(item):
    if player.CanSeeColor:
        blt.puts(item.x, item.y, "[color=%s]%s[/color]" % (item.color, item.char))
    else:
        blt.puts(item.x, item.y, "[color=%s]%s[/color]" % ("grey", item.char))

def draw_UI():

    HeaderHeight = 4
    HeaderWidth = map_width
    HeaderFrameColor = "blue"
    #draw header frame
    for x in range(0, HeaderWidth + 1):
        for y in range(0, HeaderHeight):
            if x == 0 and y == 0:
                blt.puts(x, y, "[color=%s]╒[/color]" % HeaderFrameColor)
            elif x == 0 and y == HeaderHeight - 1:
                blt.puts(x, y, "[color=%s]╘[/color]" % HeaderFrameColor)  
            elif x == HeaderWidth and y == 0:
                blt.puts(x, y, "[color=%s]╤[/color]" % HeaderFrameColor)
            elif x == HeaderWidth and y == HeaderHeight - 1:
                blt.puts(x, y, "[color=%s]╡[/color]" % HeaderFrameColor)
            elif x == 0 or x == HeaderWidth:
                blt.puts(x, y, "[color=%s]│[/color]" % HeaderFrameColor)
            elif y == 0 or y == HeaderHeight - 1:
                blt.puts(x, y, "[color=%s]═[/color]" % HeaderFrameColor)


    blt.puts(1, 1, "[color=%s]%s[/color]" % ("orange", player.name))
    blt.puts(1, 2, "[color=%s]%s[/color]" % ("darker orange", TurnCount))
    blt.puts(len(player.name) + 8, 1, "[color=%s]Health: %s[/color]" % ("green", player.Health))
    blt.puts(len(player.name) + 20, 1, "[color=%s]Life Support: %s[/color]" % ("yellow", player.LifeSupport))
    blt.puts(len(player.name) + 40, 1, "[color=%s]Aiming: %s[/color]" % ("red", Aiming))
    blt.puts(len(player.name) + 60, 1, "[color=%s]Angst: %s[/color]" % ("purple", player.angst))

    MsgFrameHeight = screen_height
    MsgFrameWidth = 20
    MsgFrameColor = "blue"
    #draw header frame
    for x in range(0, MsgFrameWidth):
        for y in range(0, MsgFrameHeight):
            if x == 0 and y == 0:
                blt.puts(x + HeaderWidth, y, "[color=%s]╤[/color]" % MsgFrameColor)
            elif x == 0 and y == MsgFrameHeight - 1:
                blt.puts(x + HeaderWidth, y, "[color=%s]╘[/color]" % MsgFrameColor)  
            elif x == MsgFrameWidth - 1 and y == 0:
                blt.puts(x + HeaderWidth, y, "[color=%s]╕[/color]" % HeaderFrameColor)
            elif x == MsgFrameWidth - 1 and y == MsgFrameHeight - 1:
                blt.puts(x + HeaderWidth, y, "[color=%s]╛[/color]" % HeaderFrameColor)
            elif x == 0 and y == HeaderHeight - 1:
                blt.puts(x + HeaderWidth, y, "[color=%s]╡[/color]" % HeaderFrameColor)
            elif x == 0 or x == MsgFrameWidth - 1:
                blt.puts(x + HeaderWidth, y, "[color=%s]│[/color]" % HeaderFrameColor)
            elif y == 0 or y == MsgFrameHeight - 1:
                blt.puts(x + HeaderWidth, y, "[color=%s]═[/color]" % HeaderFrameColor) 


    #blt.puts(0, 0, "[color=%s]╒══════════════════════════════════════════════════════════════════════════════╕[/color]" % ("darker orange"))

    #can they see layers?
    #print(len(items_present))
    if player.CanSenseLayers or len(items_present) == 0:
        blt.puts(len(player.name) + 8, 2, "[color=%s]Here: %s[/color]" % ("blue", items_present_str))
    elif not player.CanSenseLayers:
        blt.puts(len(player.name) + 8, 2, "[color=%s]Here: %s[/color]" % ("blue", items_present[0].name))
    

    y = 1
    for message in message_log.messages:
        blt.puts(map_width + 1, y, "[color=%s]%s[/color]" % (message.color, message.text))
        y += 1

def DrawCharSheet():
    blt.layer(0)
    blt.bkcolor("blue")

    for x in range(5, screen_width - 5):
        for y in range(5, screen_height - 5):
            blt.puts(x, y, "[color=red][bkcolor=blue]X[/bkcolor][/color]")
   
    blt.layer(0)

def DrawReticle():
    if Aiming:
        blt.layer(250)
        blt.puts(TargetX, TargetY, "[color=red]X[/color]")

def DrawProjectile(points):
    blt.layer(251)
    render_all(entities, gamemap)
    lx = -1
    ly = -1

    for i in range(0, len(points) - 1):
        blt.puts(points[i][0], points[i][1], "[color=cyan]*[/color]")
        if lx >= 0:
            blt.puts(lx, ly, "[color=black] [/color]")
            blt.clear_area(lx, ly, 1, 1)
            blt.refresh()
        lx = points[i][0]
        ly = points[i][1]

        blt.refresh()

    # for i in range(0, len(px) - 1):
    #     blt.puts(int(px[i]), int(py[i]), "[color=cyan]*[/color]")
    #     if lx >= 0:
    #         blt.puts(lx, ly, "[color=black] [/color]")
    #         blt.clear_area(lx, ly, 1, 1)
    #         blt.refresh()
    #         lx = px[i]
    #         ly = py[i]
    #     blt.refresh() 
    blt.clear()  
    


def clear_entity(entity):
    # erase the character that represents this object
    blt.puts(entity.x, entity.y, " ")

def update_items_present():
    items_present = []


    for i in items:
        if i.x == player.x and i.y == player.y:
            items_present.append(i)
    

    return items_present

def update_items_present_str():
    items_present_str = ""
    scount = 0
    for i in items_present:
        if scount > 0:
            items_present_str += ", "
        items_present_str += i.name
        scount += 1
    
    #message_log.add_message(Message(items_present_str))

    return items_present_str

def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def FireProjectile(tx, ty):
    # px = []
    # py = []
    # deltax = tx - player.x
    # if deltax == 0: deltax = sys.float_info.epsilon
    # deltay = ty - player.y
    # deltaerr = abs(deltay / deltax)    ## Assume deltax != 0 (line is not vertical),
    #        ## note that this division needs to be done in a way that preserves the fractional part
    # error = 0.0 ## No error at start
    # cy = player.y
    # for cx in range(player.x, tx + 1):
    #     error = error + deltaerr
    #     if error >= 0.5:
    #         cy = cy + math.copysign(1, deltay) * 1
    #         error = error - 1.0
    #     px.append(cx)
    #     py.append(cy)
    ProjectilePath = get_line((player.x, player.y),(tx, ty))
    DrawProjectile(ProjectilePath)
    return False

fps_update_time = time()
fps_counter = fps_value = 0



items = []
items_present = []
items_present_str = ""
entities = []
Menus = []

score = 0

screen_height = 50
screen_width = 80

map_height = 50
map_width = 60

gamemap = map.GameMap(map_width, map_height)

message_log = MessageLog(20, screen_width - map_width, screen_height)

blt.open()
blt.set("window: size=%ix%i, cellsize=auto, title='SFRL';" % (screen_width, screen_height))
blt.set("font: ./PressStart2P.ttf, size=10")
blt.set("output.vsync=false")
blt.composition(False)


#drop some items
for n in range(0, 10):
    randx, randy = 0, 0
    while gamemap.tiles[randx][randy].blocked:
        randx = random.randint(10, map_width - 10)
        randy = random.randint(10, map_height - 10)
    tempitem = Item(randx, randy, "Slime", '~', "dark green")
    tempitem.mutat_value = 5
    items.append(tempitem)

for n in range(0, 10):
    randx, randy = 0, 0
    while gamemap.tiles[randx][randy].blocked:
        randx = random.randint(10, map_width - 10)
        randy = random.randint(10, map_height - 10)
    tempitem = Item(randx, randy, "Battery", '(', "yellow")
    tempitem.nutra_value = -10
    tempitem.mutat_value = 1
    items.append(tempitem)


#drop some items
for n in range(0, 10):
    randx, randy = 0, 0
    while gamemap.tiles[randx][randy].blocked:
        randx = random.randint(10, map_width - 10)
        randy = random.randint(10, map_height - 10)
    tempitem = Item(randx, randy, "Garbage", '%', "white")
    tempitem.nutra_value = -5
    items.append(tempitem)

#find player starting point
randx, randy = 0, 0
while gamemap.tiles[randx][randy].blocked:
    randx = random.randint(10, map_width - 10)
    randy = random.randint(10, map_height - 10)   
player = Player(randx, randy, "Player", 'љ[+]º', "darker cyan", True, True)
entities.append(player)

##spawn some enemies
for n in range(10):
    randx, randy = 0, 0
    while gamemap.tiles[randx][randy].blocked:
        randx = random.randint(10, map_width - 10)
        randy = random.randint(10, map_height - 10)
    npc = Entity(randx, randy, "NPC", 'Ő', "pink")
    entities.append(npc)

############################main game loop
############################main game loop
############################main game loop

KeysAllowed = [blt.TK_SPACE, blt.TK_LEFT, blt.TK_RIGHT, blt.TK_UP, blt.TK_DOWN, blt.TK_ESCAPE, blt.TK_C, blt.TK_V, blt.TK_E, blt.TK_P, blt.TK_F]
Aiming = False
TargetX = 0
TargetY = 0

TurnCount = 0
TickCount = 0

while TurnCount >= 0:

    fps_counter += 1
    tm = time()
    if tm > fps_update_time + 1:
        fps_value = fps_counter
        fps_counter = 0
        fps_update_time = tm




    IncrementTurn = False
    blt.clear()


    if blt.has_input():  
        key = blt.read()
        while TurnCount > 0:
            if key in KeysAllowed:
                break
            else:
                key = blt.read()

        if Aiming:
            if (key == blt.TK_LEFT):
                TargetX -= 1
            elif (key == blt.TK_RIGHT):
                TargetX += 1
            elif (key == blt.TK_UP):
                TargetY -= 1
            elif (key == blt.TK_DOWN):
                TargetY += 1
            elif (key == blt.TK_F):
                Aiming = FireProjectile(TargetX, TargetY)             
            elif (key == blt.TK_ESCAPE):
                Aiming = False
        else:    
            if (key == blt.TK_LEFT) and not gamemap.is_blocked(player.x-1, player.y):
                player.move(-1,0)
                IncrementTurn = True
            elif (key == blt.TK_RIGHT) and not gamemap.is_blocked(player.x+1, player.y):
                player.move(1,0)
                IncrementTurn = True
            elif (key == blt.TK_UP) and not gamemap.is_blocked(player.x, player.y-1):
                player.move(0,-1)
                IncrementTurn = True
            elif (key == blt.TK_DOWN) and not gamemap.is_blocked(player.x, player.y+1):
                player.move(0,1)
                IncrementTurn = True
            elif (key == blt.TK_ESCAPE):
                exit()
            elif (key == blt.TK_C):
                player.CanSeeColor = not player.CanSeeColor
                message_log.add_message(Message("Color Vision Toggled"))
            elif (key == blt.TK_F):
                print("pressed F")
                TargetX = player.x
                TargetY = player.y
                Aiming = True           
            elif (key == blt.TK_P):
                message_log.add_message(Message("TEST PASS"))
            elif (key == blt.TK_SPACE):
                IncrementTurn = True
            elif (key == blt.TK_V):
                player.CanSenseLayers = not player.CanSenseLayers
                message_log.add_message(Message("Layer Sense Toggled"))
            elif (key == blt.TK_E):
                IncrementTurn = player.ConsumeItemFromFloor()                   
        

    if IncrementTurn:
        TurnCount += 1
        # entities try to randomly move
        for ent in entities:
            if ent != player:
                dir = random.randint(1,4)
                if dir == 1:
                    ent.move(-1,0)
                elif dir == 2:
                    ent.move(1,0)
                elif dir == 3:
                    ent.move(0,1)
                elif dir == 4:
                    ent.move(0,-1)

    #items_present = update_items_present()
    #items_present_str = update_items_present_str()
    render_all(entities, gamemap)
    blt.refresh()
    #TickCount += 1
