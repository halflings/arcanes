import random

class Character(object):
    MAX_DEXTERITY = 100.

    def __init__(self, max_hp, max_mp, strength, dexterity):
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.hp = self.max_hp
        self.mp = self.max_mp

        self.strength = strength
        self.dexterity = dexterity

    @property
    def alive(self):
        return self.hp > 0

    def attack(self, enemy):
        attack = self.strength * (0.8 + 0.2*random.random())
        defense = enemy.dexterity * (0.8 + 0.2*random.random())

        # damage = attack - % protected by the calculated defense (defense/MAX_DEXTERITY)
        damage = attack * (1. - (defense/Character.MAX_DEXTERITY))
        if attack < 0:
            return None
        enemy.hp -= damage
        return damage

class Player(Character):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.xp = 0
        self.level = 1

    @property
    def upgrade_xp(self):
        return 10 + 20 * self.level**2

    def killed(self, enemy):
        self.xp += enemy.attack * 2 + enemy.defense * 3

        # Potentially upgrading level(s) due to won XP
        while self.xp > self.upgrade_xp:
            self.xp -= self.upgrade_xp
            self.level += 1