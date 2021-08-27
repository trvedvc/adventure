import arcade
from math import *

# Constants
TILE_WIDTH = 64
TILECOUNTX = 15
TILECOUNTY = 8
SCREEN_WIDTH = TILECOUNTX * TILE_WIDTH
SCREEN_HEIGHT = TILECOUNTY * TILE_WIDTH
SCREEN_TITLE = "adventure"

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1


def load_weapon_texture_pair(filename, hit_box_algorithm: str = "Simple"):  # Default: "Simple"
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename,
                            hit_box_algorithm=hit_box_algorithm),
        arcade.load_texture(filename,
                            flipped_vertically=True,
                            hit_box_algorithm=hit_box_algorithm)
    ]


def load_texture_pair(filename, hit_box_algorithm: str = "Simple"):
    """
    Load a texture pair, with the second being a mirror image of the first.
    Useful when doing animations and the character can face left/right.
    """
    return [
        arcade.load_texture(filename,
                            hit_box_algorithm=hit_box_algorithm),
        arcade.load_texture(filename,
                            flipped_horizontally=True,
                            hit_box_algorithm=hit_box_algorithm)
    ]


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

    def giveWeapon(self):  # TODO self.hand_left/right

        main_path = "sword/sword"

        # Load textures for idle weapon
        self.idle_texture_pair = load_weapon_texture_pair(f"{main_path}1.png")

        # Load textures for weapon swing
        self.swing_textures = []
        for i in range(1, 4):
            texture = load_weapon_texture_pair(f"{main_path}{i}.png")
            self.swing_textures.append(texture)

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
        self.weapons = Weapon()
        self.weapons.center_x = 32 + TILE_WIDTH + 5
        self.weapons.center_y = 32 - TILE_WIDTH - 5
        self.weapon_list.append(self.weapons)

        # --- Load Textures ---

        # Images for walking
        main_path = "player_moves/player"

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

        self.shadowCenter = arcade.Sprite("shadow/shadowCenter.png", 0.5)
        self.shadowTop = arcade.Sprite("shadow/shadow1.png", 0.5)
        self.shadowBot = arcade.Sprite("shadow/shadow1.png", 0.5)
        self.shadowLeft = arcade.Sprite("shadow/shadow2.png", 0.5)
        self.shadowRight = arcade.Sprite("shadow/shadow2.png", 0.5)

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


class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color([13, 9, 9])
        # arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.tile_list = arcade.SpriteList()
        self.collider_list = arcade.SpriteList()

        self.listLogicalMap = []

        self.creatingGraphicalMapByLogicalMap(self.listLogicalMap)

        self.enemy_list = arcade.SpriteList()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.mouse_moved = False

    def creatingGraphicalMapByLogicalMap(self, listLogicalMap):  # vykreslení políček

        # přečte z texťáku s mapou písmenka a přepíše je do 2 rozměrného pole
        with open("logical_map_layout_test.txt", 'r') as logicalMap:
            x = TILE_WIDTH // 2
            y = TILE_WIDTH // 2
            for lineOfLogicalMap in logicalMap:
                self.listLogicalMap.append([])
                for charInLineOfLogicalMap in lineOfLogicalMap:
                    if charInLineOfLogicalMap != "\n":
                        self.listLogicalMap[len(self.listLogicalMap) - 1].append(charInLineOfLogicalMap)

        # projíždí prvky pole a pokud políčko není zobrazeno jako prázdné, tak se vykreslí políčko
        xCounterList = 0
        yCounterList = 0
        for lineOfLogicalMap2 in listLogicalMap:
            for charInLineOfLogicalMap2 in lineOfLogicalMap2:
                if charInLineOfLogicalMap2 != "-":
                    tile = arcade.Sprite("textura_podlaha128.png", 0.5)
                    tile.center_x = x
                    tile.center_y = y
                    self.tile_list.append(tile)

                    # pokud se stane, že políčko vedle právě vykreslovaného je prázdné, tak se správně otočí a zobrazí textura zdi
                    # ktery CounterList, horni/spodni rada, yCounter check, xCounter check, úhel
                    RotationPossibilities = [[yCounterList, 0, -1, 0, -90],  # top
                                             [xCounterList, 0, 0, -1, 0],  # left
                                             [yCounterList, len(listLogicalMap) - 1, 1, 0, 90],  # bottom
                                             [xCounterList, len(listLogicalMap[0]) - 1, 0, 1, 180]]  # right

                    for indexRotationPossibilities in RotationPossibilities:
                        irp = indexRotationPossibilities
                        if irp[0] == irp[1] or listLogicalMap[yCounterList + irp[2]][xCounterList + irp[3]] == "-":
                            tile_wall = arcade.Sprite("textura_zed128.png", 0.5)
                            tile_wall.angle = irp[4]
                            tile_wall.center_x = x
                            tile_wall.center_y = y
                            self.tile_list.append(tile_wall)

                            if irp[4] == -90:
                                tile_invisible_barrier = arcade.Sprite("invisible_wall_barrierT.png", 0.5)
                            else:
                                tile_invisible_barrier = arcade.Sprite("invisible_wall_barrierLRB.png", 0.5)
                                tile_invisible_barrier.angle = irp[4]
                            tile_invisible_barrier.center_x = x
                            tile_invisible_barrier.center_y = y
                            tile_invisible_barrier.alpha = 0
                            self.collider_list.append(tile_invisible_barrier)

                if charInLineOfLogicalMap2 == "c":
                    tile_chest = arcade.Sprite("shitty_chest.png", 0.5)
                    tile_chest.center_x = x
                    tile_chest.center_y = y
                    self.tile_list.append(tile_chest)

                x += TILE_WIDTH
                xCounterList += 1
            # print(yCounterList, xCounterList)
            y -= TILE_WIDTH
            x = TILE_WIDTH // 2
            yCounterList += 1
            xCounterList = 0

    def spawnEnemy(self, coords):

        enemy = Enemy()
        enemy.center_x, enemy.center_y = coords
        enemy.update_healthBar()
        self.enemy_list.append(enemy)

    def set_vsync(self, vsync: bool):
        """ Set if we sync our draws to the monitors vertical sync rate. """
        super().set_vsync(vsync)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Setup player
        self.player_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.player.center_x = 32 + TILE_WIDTH
        self.player.center_y = 32 - TILE_WIDTH
        self.player_list.append(self.player)
        self.player.createShadow()
        self.player.weapons.giveWeapon()

        # Setup enemies
        self.spawnEnemy([32 + TILE_WIDTH * 2, 32 - TILE_WIDTH])

        # self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.collider_list, gravity_constant = 0)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        # Draw map
        self.tile_list.draw()
        self.collider_list.draw()

        # Draw player
        self.player.shadow_list.draw()
        self.player_list.draw()
        self.player.weapon_list.draw()

        # Draw enemy
        self.enemy_list.draw()

        for enemy in self.enemy_list:  # TODO ? spritelist
            enemy.healthBar.draw()

        # Draw hit boxes
        self.player.draw_hit_box()
        self.player.weapons.draw_hit_box()
        self.enemy_list.draw_hit_boxes()
        self.player.shadow_list.draw_hit_boxes()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        """self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0"""

        # self.physics_engine.update()

        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed and len(
                self.player.shadowTop.collides_with_list(self.tile_list)) > 0 and len(
                arcade.check_for_collision_with_list(self.player.shadowTop, self.collider_list)) < 1:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed and len(
                self.player.shadowBot.collides_with_list(self.tile_list)) > 0 and len(
                arcade.check_for_collision_with_list(self.player.shadowBot, self.collider_list)) < 1:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed and len(
                self.player.shadowLeft.collides_with_list(self.tile_list)) > 0 and len(
                arcade.check_for_collision_with_list(self.player.shadowLeft, self.collider_list)) < 1:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed and len(
                self.player.shadowRight.collides_with_list(self.tile_list)) > 0 and len(
                arcade.check_for_collision_with_list(self.player.shadowRight, self.collider_list)) < 1:
            self.player.change_x = MOVEMENT_SPEED

        if len(arcade.check_for_collision_with_list(self.player.shadowCenter, self.collider_list)) > 0:
            print("Vlezl jsi do bariéry. GG WP")

        # DMG dealing to enemies
        self.hit_enemies = self.player.weapons.collides_with_list(self.enemy_list)

        if len(self.hit_enemies) > 0:
            for enemy in self.hit_enemies:
                if enemy.can_be_hit and self.player.weapons.attack:
                    print(enemy.hp_cur)
                    enemy.hp_cur -= 1
                    enemy.update_healthBar()
                    enemy.can_be_hit = False
                    if enemy.hp_cur == 0:
                        self.enemy_list.remove(enemy)
                if not self.player.weapons.attack:
                    enemy.can_be_hit = True

        self.player_list.update()
        self.player_list.update_animation()
        self.player.weapon_list.update_animation()

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.

        # ?
        arcade.set_viewport(self.player.center_x - SCREEN_WIDTH / 2,
                            self.player.center_x + SCREEN_WIDTH / 2,
                            self.player.center_y - SCREEN_HEIGHT / 2,
                            self.player.center_y + SCREEN_HEIGHT / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player.weapons.can_swing:
            self.player.weapons.attack = True
            self.player.weapons.can_swing = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.player.weapons.attack is not True:
            if x < SCREEN_WIDTH / 2 and self.player.character_face_direction == RIGHT_FACING:
                self.player.character_face_direction = LEFT_FACING
                self.player.weapons.face_dir = LEFT_FACING
            elif x > SCREEN_WIDTH / 2 and self.player.character_face_direction == LEFT_FACING:
                self.player.character_face_direction = RIGHT_FACING
                self.player.weapons.face_dir = RIGHT_FACING
            self.player.weapons.cursor_pos_x = x
            self.player.weapons.cursor_pos_y = y
            self.player.weapons.findAngle()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
