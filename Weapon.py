import arcade
from math import *
from Texture import *

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

class Weapon(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.attack = False
        self.can_swing = True
        self.swing_start = True
        self.swing_angle = 90
        self.angle_dif = [-6, 6]

        self.cursor_pos_x = 0
        self.cursor_pos_y = 0

        self.cur_weapon_texture = 0
        self.face_dir = RIGHT_FACING
        self.scale = 2

    def giveWeapon(self, weapon):  # TODO self.hand_left/right

        self.idle_texture_pair = load_weapon_texture_pair(weapon)
        self.texture = self.idle_texture_pair[self.face_dir]

    def findAngle(self):

        vector_x = self.cursor_pos_x - SCREEN_WIDTH / 2
        vector_y = self.cursor_pos_y - SCREEN_HEIGHT / 2
        if vector_x != 0:
            angle = degrees(atan(vector_y / vector_x))
            if self.cursor_pos_x > SCREEN_WIDTH / 2:
                self.angle = angle
            else:
                self.angle = 180 + angle
        else:
            if self.cursor_pos_y < SCREEN_HEIGHT / 2:
                self.angle = 270
            elif self.cursor_pos_y > SCREEN_HEIGHT / 2:
                self.angle = 90

    def update_animation(self, delta_time: float = 1 / 60):
        # Idle weapon ??
        if not self.attack:
            self.texture = self.idle_texture_pair[self.face_dir]
            return

        # Weapon swing
        if self.attack:
            if self.swing_start:
                self.angle -= self.swing_angle / 2 * (self.angle_dif[self.face_dir] / self.angle_dif[1])
                self.swing_start = False
            else:
                if self.swing_angle > 0:
                    self.swing_angle += self.angle_dif[0]
                    self.angle += self.angle_dif[self.face_dir]
                else:
                    self.swing_angle = 90
                    self.attack = False
                    self.can_swing = True
                    self.swing_start = True
                    self.findAngle()
