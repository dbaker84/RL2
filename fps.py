from bearlibterminal import terminal as blt
from time import time


fps_update_time = time()
fps_counter = fps_value = 0

screen_height = 50
screen_width = 80


blt.open()
blt.set("window: size=%ix%i, cellsize=auto, title='SFRL';" % (screen_width, screen_height))
blt.set("font: ./PressStart2P.ttf, size=10")
blt.set("output.vsync=false")
blt.composition(True)

Proceed = True
Aiming = False
TurnCount = 0
entities = []
TargetX = TargetY = 0

while Proceed:

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
                Aiming = True            
            elif (key == blt.TK_ESCAPE):
                Aiming = False
        else:    
            if (key == blt.TK_LEFT):
                pass                  
        

    if IncrementTurn:
        TurnCount += 1
        # entities try to randomly move
        for ent in entities:
            pass

    #items_present = update_items_present()
    #items_present_str = update_items_present_str()
    blt.puts(0,0,"%s" % fps_value)
    # render_all(entities, gamemap)
    blt.refresh()
    #TickCount += 1
