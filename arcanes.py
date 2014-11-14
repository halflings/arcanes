import numpy as np
import pyglet

from particles import ParticleEmitter

class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)

        # Setting up OpenGL context
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Setting the resource path
        pyglet.resource.path = ['images']
        pyglet.resource.reindex()

        # Setting up the particle emitter
        init_pos = np.array([self.width/2., self.height/2.])
        color = np.array([190, 190, 255])
        self.particle_emitter = ParticleEmitter(max_particles=4000, position=init_pos, particle_lifetime=1., emission_frequency=200.,
                                                emission_speed=1.5, particle_size=1, color=color)
        self.particle_emitter.emitting = False

        # Background image
        self.bg_texture = pyglet.resource.image('stone.png')
        self.bg_tiling = pyglet.image.TileableTexture.create_for_image(self.bg_texture)

        # Update event
        self.fps = 80.
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps)

        # Array used to save the coordinates the mouse went through while casting
        self.gesture_coordinates = []

        # FPS display, for debugging
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()

        self.bg_tiling.blit_tiled(0, 0, 0, self.width, self.height)

        self.particle_emitter.draw()

        self.fps_display.draw()

    def update(self, dt):
        self.particle_emitter.update(dt)

    def new_position(self, x, y):
        position = np.array([float(x), float(y)])
        self.particle_emitter.position = position
        self.gesture_coordinates.append(position)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.new_position(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.new_position(x, y)
        self.particle_emitter.emitting = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.particle_emitter.emitting = False

        # TODO: exploit the gesture's coordinates

        # Resetting the gesture coordinates
        self.gesture_coordinates = []

if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()