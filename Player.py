import arcade
from math import *
from Texture import *
from Weapon import *

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = 1

        self.shadow_list = arcade.SpriteList()

        # TODO -> MyGame function?
        self.weapon_list = arcade.SpriteList()

        self.weapon_right = Weapon()
        self.weapon_list.append(self.weapon_right)

        self.weapon_left = Weapon()
        self.weapon_list.append(self.weapon_left)

        # --- Load Textures ---

        # Images for walking
        main_path = "assets/player_moves/player"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}1.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(1, 5):
            texture = load_texture_pair(f"{main_path}{i}.png")
            self.walk_textures.append(texture)

    # Netušim co se tu děje -> uz vim
    def update_animation(self, delta_time: float = 1 / 60):

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 4 * UPDATES_PER_FRAME - 1:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]

    def createShadow(self):

        self.shadowCenter = arcade.Sprite("assets/shadow/shadowCenter.png", 0.5)
        self.shadowTop = arcade.Sprite("assets/shadow/shadow1.png", 0.5)
        self.shadowBot = arcade.Sprite("assets/shadow/shadow1.png", 0.5)
        self.shadowLeft = arcade.Sprite("assets/shadow/shadow2.png", 0.5)
        self.shadowRight = arcade.Sprite("assets/shadow/shadow2.png", 0.5)

        flip = False
        shadows = [self.shadowTop, self.shadowBot, self.shadowLeft, self.shadowRight, self.shadowCenter]

        for shadow in shadows:
            if flip:
                shadow.angle = 180
                flip = False
            else:
                flip = True
            shadow.center_x = self.center_x
            shadow.center_y = self.center_y - 19
            self.shadow_list.append(shadow)

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.shadow_list.move(self.change_x, self.change_y)
        self.weapon_list.move(self.change_x, self.change_y)
