import arcade
from math import *
from Player import *
from Texture import *
from Enemy import *
import operator

# Constants
TILE_WIDTH = 64
TILECOUNTX = 15
TILECOUNTY = 8
SCREEN_WIDTH = TILECOUNTX * TILE_WIDTH # ???
SCREEN_HEIGHT = TILECOUNTY * TILE_WIDTH
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_TITLE = "adventure"

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1


class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)

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

        self.mouse_moved = False # ???

        # Věci pro inventář
        self.inventory_opened = False
        self.inv_sprite_list = arcade.ShapeElementList()

    # TODO class Map
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

    def dealDMG(self,hand):
        for enemy in self.hit_enemies:
            if enemy.can_be_hit:
                if self.player.weapon_right.attack and hand == "right":
                    enemy.hp_cur -= 1
                    enemy.can_be_hit = False
                if self.player.weapon_left.attack and hand == "left":
                    enemy.hp_cur -= 1
                    enemy.can_be_hit = False
                enemy.update_healthBar()
                if enemy.hp_cur == 0:
                    self.enemy_list.remove(enemy)
            if not self.player.weapon_right.attack and not self.player.weapon_left.attack:
                enemy.can_be_hit = True

    def drawInventory(self): #TODO
        bigChunk = arcade.create_rectangle_filled(self.player.center_x + SCREEN_WIDTH/4,
                                                  self.player.center_y,
                                                  SCREEN_WIDTH/5*2,
                                                  SCREEN_HEIGHT/5*4, arcade.csscolor.RED)
        self.inv_sprite_list.append(bigChunk)

    def set_vsync(self, vsync: bool):
        """ Set if we sync our draws to the monitors vertical sync rate. """
        super().set_vsync(vsync)

    def setup(self): # TODO package
        """ Set up the game here. Call this function to restart the game. """

        # Setup player
        self.player_list = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.player.center_x = 32 + TILE_WIDTH
        self.player.center_y = 32 - TILE_WIDTH
        self.player_list.append(self.player)
        self.player.createShadow()

        self.player.weapon_right.giveWeapon("assets/weapons/sword.png") # TODO ? func
        self.player.weapon_right.center_x = self.player.center_x + 5
        self.player.weapon_right.center_y = self.player.center_y - 5

        self.player.weapon_left.giveWeapon("assets/weapons/axe.png")
        self.player.weapon_left.center_x = self.player.center_x + 5
        self.player.weapon_left.center_y = self.player.center_y - 5

        # Setup enemies
        self.spawnEnemy([32 + TILE_WIDTH * 2, 32 - TILE_WIDTH])

        self.drawInventory()

        # self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.collider_list, gravity_constant = 0)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        # Draw map
        self.tile_list.draw()
        self.collider_list.draw()

        # Draw first weapon; if RIGHT_FACING: draw weapon_left
        self.player.weapon_list[self.player.character_face_direction - 1].draw()

        # Draw player
        self.player.shadow_list.draw()
        self.player_list.draw()

        # Draw 2nd weapon
        self.player.weapon_list[self.player.character_face_direction].draw()

        # Draw enemy
        self.enemy_list.draw()

        # Draw inventory
        # if len(self.inv_sprite_list) == 1:
        if self.inventory_opened:
            self.inv_sprite_list.draw()

        for enemy in self.enemy_list:  # TODO ? spritelist
            enemy.healthBar.draw()

        # Draw hit boxes
        self.player.draw_hit_box()
        self.player.weapon_list.draw_hit_boxes()
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
        if len(self.player.weapon_right.collides_with_list(self.enemy_list)) > 0:
            #print("right")
            self.hit_enemies = self.player.weapon_right.collides_with_list(self.enemy_list)
            self.dealDMG("right")
        if len(self.player.weapon_left.collides_with_list(self.enemy_list)) > 0:
            #print("left")
            self.hit_enemies = self.player.weapon_left.collides_with_list(self.enemy_list)
            self.dealDMG("left")

        # Pohyb inventářem po obrazovce
        self.inv_sprite_list.move(self.player.change_x, self.player.change_y)

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
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.player.weapon_right.can_swing and not self.player.weapon_left.attack:
                self.player.weapon_right.attack = True
                self.player.weapon_right.can_swing = False
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.player.weapon_left.can_swing and not self.player.weapon_right.attack:
                self.player.weapon_left.attack = True
                self.player.weapon_left.can_swing = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        if self.player.weapon_right.attack is not True:
            if x < SCREEN_WIDTH/2 and self.player.character_face_direction == RIGHT_FACING:
                self.player.character_face_direction = LEFT_FACING
                self.player.weapon_right.face_dir = LEFT_FACING
                self.player.weapon_left.face_dir = LEFT_FACING
                self.player.weapon_right.center_y = self.player.center_y - 5 + 5
                self.player.weapon_left.center_y = self.player.center_y - 5

            elif x > SCREEN_WIDTH/2 and self.player.character_face_direction == LEFT_FACING:
                self.player.character_face_direction = RIGHT_FACING
                self.player.weapon_right.face_dir = RIGHT_FACING
                self.player.weapon_left.face_dir = RIGHT_FACING
                self.player.weapon_right.center_y = self.player.center_y - 5
                self.player.weapon_left.center_y = self.player.center_y - 5 + 5

            # cancer ngl
            self.player.weapon_right.cursor_pos_x = x
            self.player.weapon_right.cursor_pos_y = y
            self.player.weapon_right.findAngle()

            self.player.weapon_left.cursor_pos_x = x
            self.player.weapon_left.cursor_pos_y = y
            self.player.weapon_left.findAngle()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        """Tlačítka pro pohyb"""
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

        # Tlačítka pro inventář
        if key == arcade.key.TAB:
            self.inventory_opened = operator.not_(self.inventory_opened)

        """if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)"""

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False




def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()