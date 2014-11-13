import random

import numpy as np
import pyglet

class PhysicalObject(object):
    def __init__(self, position, velocity=None, acceleration=None, damping=0.):
        self.position = position
        self.velocity = velocity
        self.damping = damping
        if self.velocity is None:
            self.velocity = np.array([0., 0.])
        self.acceleration = acceleration
        if self.acceleration is None:
            self.acceleration = np.array([0., 0.])

    def update(self, dt):
        self.position = self.position + dt * self.velocity
        self.velocity = (1 - self.damping * dt) * self.velocity + dt * self.acceleration

class ParticleEmitter(PhysicalObject):
    def __init__(self, max_particles, particle_lifetime, emission_frequency, color, *args, **kwargs):
        super(ParticleEmitter, self).__init__(*args, **kwargs)
        self.max_particles = max_particles
        self.emission_frequency = emission_frequency
        self.color = color
        self.particle_lifetime = particle_lifetime

        self.time_last_emission = 0.
        self.emitting = True
        self.particles = list()

    def emit_particle(self):
        color = self.color + np.random.random_integers(100, 200, 3)
        color = 255 * color / max(color)

        speed = 20.
        velocity = np.random.ranf(2) * speed - speed / 2.
        damping = random.random()
        position = self.position
        lifetime = self.particle_lifetime * (0.8 + 0.2 * random.random())
        return Particle(color=color, lifetime=lifetime,
                        position=position, velocity=velocity, damping=damping)

    def update(self, dt):
        super(ParticleEmitter, self).update(dt)

        self.time_last_emission += dt
        scheduled_emissions = int(self.time_last_emission * self.emission_frequency)
        empty_spots = self.max_particles - len(self.particles)
        if empty_spots > 0 and self.emitting and scheduled_emissions > 0:
            for i in xrange(min(scheduled_emissions, empty_spots)):
                self.particles.append(self.emit_particle())
            self.time_last_emission = 0.

        for i, particle in enumerate(self.particles):
            particle.update(dt)
            if not particle.alive and self.emitting:
                self.particles[i] = self.emit_particle()


    def draw(self):
        batch = pyglet.graphics.Batch()
        for particle in self.particles:
            if particle.alive:
                particle.draw(batch)
        batch.draw()

class Particle(PhysicalObject):
    def __init__(self, color, lifetime, *args, **kwargs):
        super(Particle, self).__init__(*args, **kwargs)
        self.color = color
        self.lifetime = lifetime

        size = 1
        self.vertices = np.hstack([self.position + [-size, size], self.position + [-size, -size], self.position + [size, 0]])
        self.vertices_colors = np.hstack([self.color] * 3)

    def update(self, dt):
        super(Particle, self).update(dt)
        self.lifetime -= dt

        self.vertices = self.vertices + np.hstack([self.velocity] * 3)

    @property
    def alive(self):
        return self.lifetime > 0

    def draw(self, batch):
        batch.add(3, pyglet.gl.GL_TRIANGLES, None,
            ('v2f', self.vertices),
            ('c3B', self.vertices_colors)
        )
