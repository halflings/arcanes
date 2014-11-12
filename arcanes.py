import pyglet

class GameWindow(pyglet.window.Window):
    def __init__(self):
        super(GameWindow, self).__init__()

        self.label = pyglet.text.Label('Hello, world!')

    def on_draw(self):
        self.clear()
        self.label.draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        print "Mouse dragged to", x, y

    def on_mouse_press(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    window = GameWindow()
    pyglet.app.run()