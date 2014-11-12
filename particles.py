import random

import numpy as np
import pyglet

class PhysicalObject(object):
    def __init__(self, position, velocity=None, acceleration=None):
        self.position = position
        self.velocity = velocity
        if self.velocity is None:
            self.velocity = np.array([0., 0.])
        self.acceleration = acceleration
        if self.acceleration is None:
            self.acceleration = np.array([0., 0.])

    def update(self, dt):
        self.position = self.position + dt * self.velocity
        self.velocity = self.velocity + dt * self.acceleration

class ParticleEmitter(PhysicalObject):
    def __init__(self, max_particles, particle_lifetime, emission_frequency, color, *args, **kwargs):
        super(ParticleEmitter, self).__init__(*args, **kwargs)
        self.max_particles = max_particles
        self.emission_frequency = emission_frequency
        self.color = color
        self.time_last_emission = 0.
        self.particle_lifetime = particle_lifetime

        self.particles = list()
        #self.emit()

    def emit(self):
        for i in xrange(self.max_particles - len(self.particles)):
            emitted_particle = self.emit_particle()
            self.particles.append(emitted_particle)

    def emit_particle(self):
        color = self.color + np.random.random_integers(100, 200, 3)
        color = 255 * color / max(color)

        speed = 40.
        velocity = np.random.ranf(2) * speed - speed / 2.
        acceleration = - random.random() * velocity
        position = self.position
        return Particle(color=color, lifetime=self.particle_lifetime,
                        position=position, velocity=velocity, acceleration=acceleration)

    def update(self, dt):
        super(ParticleEmitter, self).update(dt)

        self.time_last_emission += dt
        if len(self.particles) < self.max_particles and self.time_last_emission > 1.0 / self.emission_frequency:
            for i in xrange(int(self.time_last_emission * self.emission_frequency)):
                self.particles.append(self.emit_particle())
            self.time_last_emission = 0.

        for i, particle in enumerate(self.particles):
            particle.update(dt)
            if not particle.alive:
                self.particles[i] = self.emit_particle()


    def draw(self):
        batch = pyglet.graphics.Batch()
        for particle in self.particles:
            particle.draw(batch)
        batch.draw()

class Particle(PhysicalObject):
    def __init__(self, color, lifetime, *args, **kwargs):
        super(Particle, self).__init__(*args, **kwargs)
        self.color = color
        self.lifetime = lifetime

    def update(self, dt):
        super(Particle, self).update(dt)
        self.lifetime -= dt

    @property
    def alive(self):
        return self.lifetime > 0

    def draw(self, batch):
        batch.add(1, pyglet.gl.GL_POINTS, None,
            ('v2f', self.position),
            ('c3B', self.color)
        )
