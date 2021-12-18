import arcade
from math import *
from Texture import *
from Weapon import *

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

class Enemy(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.hp_max = 5
        self.hp_cur = self.hp_max
        self.texture = arcade.load_texture("ememy.png")
        self.healthBar = arcade.ShapeElementList()

        self.can_be_hit = True

    def update_healthBar(self):  # game function? TODO
        hp_percent = self.hp_cur / self.hp_max * 100

        self.healthBar = arcade.ShapeElementList()

        missingHealth = arcade.create_rectangle(self.center_x, self.top + 10, 50, 6, arcade.csscolor.GRAY)
        self.healthBar.append(missingHealth)

        health = arcade.create_rectangle(self.center_x - 25 + (hp_percent / 4), self.top + 10, hp_percent / 2, 6,
                                         arcade.csscolor.RED)
        self.healthBar.append(health)
