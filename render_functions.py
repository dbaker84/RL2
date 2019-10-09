from bearlibterminal import terminal as blt

def render_all(entities, gamemap):


    # Draw all the tiles in the game map
    blt.layer(0)
    for y in range(gamemap.height):
        for x in range(gamemap.width):
            blt.puts(x, y, "[color=%s]%s[/color]" % (gamemap.tiles[x][y].color, gamemap.tiles[x][y].char))

    blt.layer(1)
    # Draw all entities in the list
    for entity in entities:
        draw_entity(entity)
    

    blt.refresh()


def clear_all(entities):
    for entity in entities:
        clear_entity(entity)


def draw_entity(entity):
    blt.puts(entity.x, entity.y, "[color=%s]%s[/color]" % (entity.color, entity.char))


def clear_entity(entity):
    # erase the character that represents this object
    blt.puts(entity.x, entity.y, " ")