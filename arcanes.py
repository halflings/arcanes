import math

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

        # Setting-up the clock / max FPS / update event
        self.fps = 80.
        self.time = 0.
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps)

        # Setting up the particle emitter
        init_pos = np.array([self.width/2., self.height/2.])
        color = np.array([190, 190, 255])
        self.particle_emitter = ParticleEmitter(max_particles=4000, position=init_pos, particle_lifetime=1., emission_frequency=500.,
                                                emission_speed=1.5, particle_size=2, color=color)
        self.particle_emitter.emitting = False

        # Background image
        self.bg_texture = pyglet.resource.image('stone.png')
        self.bg_tiling = pyglet.image.TileableTexture.create_for_image(self.bg_texture)

        # Enemy image
        self.enemy_image = pyglet.resource.image('orc.png')
        self.enemy_image.anchor_x, self.enemy_image.anchor_y = self.enemy_image.width/2, self.enemy_image.height/2

        self.enemy_y = self.height/2 - 50
        self.enemy_base_scaling = 0.5
        self.enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, x=self.width/2, y=self.enemy_y)

        # Array used to save the coordinates the mouse went through while casting
        self.gesture_coordinates = []

        # FPS display, for debugging purposes
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()

        self.bg_tiling.blit_tiled(0, 0, 0, self.width, self.height)
        self.enemy_sprite.draw()

        self.particle_emitter.draw()

        self.fps_display.draw()

    def update(self, dt):
        self.time += dt
        self.particle_emitter.update(dt)

        time_ratio = math.sin(self.time)
        self.enemy_sprite.rotation = 5 * time_ratio
        self.enemy_sprite.y = self.enemy_y + 20 * time_ratio
        if time_ratio < 0:
            self.enemy_sprite.scale = self.enemy_base_scaling
        else:
            self.enemy_sprite.scale = self.enemy_base_scaling * (1. + 0.25 * time_ratio)

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