from bearlibterminal import terminal

terminal.open()
terminal.set("window: size=80x25, title='mygame'; font: courdb.ttf, size=18")
terminal.printf(2, 1, "c")
terminal.refresh()
while terminal.read() != terminal.TK_CLOSE:
    pass