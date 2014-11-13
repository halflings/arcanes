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
    MAX_PARTICLES = 1000
    PARTICLE_LIFETIME = 2.
    EMISSION_FREQUENCY = 200.
    COLOR = np.array([50, 190, 230])
    EMISSION_SPEED = 5.
    PARTICLE_SIZE = 3

    def __init__(self, max_particles=MAX_PARTICLES, particle_lifetime=PARTICLE_LIFETIME, particle_size=PARTICLE_SIZE,
                 emission_frequency=EMISSION_FREQUENCY, emission_speed=EMISSION_SPEED, color=COLOR,
                 *args, **kwargs):
        super(ParticleEmitter, self).__init__(*args, **kwargs)
        self.max_particles = max_particles
        self.emission_frequency = emission_frequency
        self.emission_speed = emission_speed
        self.particle_size = particle_size
        self.color = color
        self.particle_lifetime = particle_lifetime

        self.time_last_emission = 0.
        self._emitting = True
        self.particles = list()

    @property
    def emitting(self):
        return self._emitting
    @emitting.setter
    def emitting(self, value):
        self._emitting = value
        self.time_last_emission = 0.

    def emit_particle(self):
        color = self.color + np.random.random_integers(100, 200, 3)
        color = 255 * color / max(color)

        velocity = self.emission_speed * (0.5 + 0.5 * random.random()) * (np.random.ranf(2) - 0.5)
        damping = 0.5 + 0.5 * random.random()
        position = self.position
        lifetime = self.particle_lifetime * (0.8 + 0.2 * random.random())
        size = self.particle_size
        return Particle(color=color, lifetime=lifetime, size=size,
                        position=position, velocity=velocity, damping=damping)

    def update(self, dt):
        super(ParticleEmitter, self).update(dt)

        self.time_last_emission += dt
        scheduled_emissions = int(self.time_last_emission * self.emission_frequency)
        empty_spots = self.max_particles - len(self.particles)
        if empty_spots > 0 and self.emitting and scheduled_emissions > 0:
            for i, particle in enumerate(self.particles):
                if not particle.alive:
                    self.particles[i] = self.emit_particle()
                    scheduled_emissions -= 1
                if scheduled_emissions <= 0:
                    break

            for i in xrange(min(scheduled_emissions, empty_spots)):
                self.particles.append(self.emit_particle())
            self.time_last_emission = 0.

        for i, particle in enumerate(self.particles):
            if particle.alive:
                particle.update(dt)


    def draw(self):
        batch = pyglet.graphics.Batch()
        for particle in self.particles:
            if particle.alive:
                particle.draw(batch)
        batch.draw()

class Particle(PhysicalObject):
    def __init__(self, color, size, lifetime, *args, **kwargs):
        super(Particle, self).__init__(*args, **kwargs)
        self.color = color
        self.max_lifetime = lifetime
        self.lifetime = self.max_lifetime
        self.size = size

        self.vertices = np.hstack([self.position + [-size, size], self.position + [-size, -size], self.position + [size, 0]])

    def update(self, dt):
        super(Particle, self).update(dt)
        self.lifetime -= dt

        self.vertices = self.vertices + np.hstack([self.velocity] * 3)

    @property
    def alive(self):
        return self.lifetime > 0

    def draw(self, batch):
        alpha = self.lifetime/self.max_lifetime
        vertices_colors = np.hstack([np.append(self.color/255., alpha)] * 3)
        batch.add(3, pyglet.gl.GL_TRIANGLES, None,
            ('v2f', self.vertices),
            ('c4f', vertices_colors)
        )
