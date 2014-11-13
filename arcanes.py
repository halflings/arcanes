import numpy as np
import pyglet

from particles import ParticleEmitter

class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)

        init_pos = np.array([self.width/2., self.height/2.])
        color = np.array([50, 190, 230])
        self.particle_emitter = ParticleEmitter(max_particles=2000, particle_lifetime=1., emission_frequency=300.,
                                                color=color, position=init_pos)
        self.particle_emitter.emitting = False

        # Update event
        self.fps = 145.
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps)

        # FPS display, for debugging
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()

        self.particle_emitter.draw()

        self.fps_display.draw()

    def update(self, dt):
        self.particle_emitter.update(dt)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.particle_emitter.position = np.array([float(x), float(y)])

    def on_mouse_press(self, x, y, button, modifiers):
        self.particle_emitter.position = np.array([float(x), float(y)])
        self.particle_emitter.emitting = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.particle_emitter.emitting = False

if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()