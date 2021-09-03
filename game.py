#seks
import arcade
from math import *

# Constants
TILE_WIDTH = 64
TILECOUNTX = 15
TILECOUNTY = 8
SCREEN_WIDTH = TILECOUNTX * TILE_WIDTH
SCREEN_HEIGHT = TILECOUNTY * TILE_WIDTH

SCREEN_TITLE = "Lololoolol"

MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 8

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class weapon(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.attack = False
        self.cur_weapon_texture = 0
        self.face_dir = RIGHT_FACING
        self.scale = 2


    def giveWeapon(self,player_x, player_y):

        main_path = "sword/sword"

        # Load textures for idle weapon
        self.idle_texture_pair = load_texture_pair(f"{main_path}1.png")

        # Load textures for weapon swing
        self.swing_textures = []
        for i in range(1, 4):
            texture = load_texture_pair(f"{main_path}{i}.png")
            self.swing_textures.append(texture)


    def update_animation(self, delta_time: float = 1/60):
        # Idle weapon
        if not self.attack:
            self.texture = self.idle_texture_pair[self.face_dir]
            return

        # Weapon swing
        if self.attack:
            self.cur_weapon_texture += 1
            if self.cur_weapon_texture > 3 * UPDATES_PER_FRAME - 1:
                self.cur_weapon_texture = 0
                self.angle = 0
                self.attack = False
            frame = self.cur_weapon_texture // UPDATES_PER_FRAME
            direction = self.face_dir
            self.texture = self.swing_textures[frame][direction]



class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = 1
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        self.shadow_list = arcade.SpriteList()

        self.weapon_list = arcade.SpriteList()
        self.weapons = weapon()
        self.weapons.center_x = 32 + TILE_WIDTH + 5
        self.weapons.center_y = 32 - TILE_WIDTH - 5
        self.weapon_list.append(self.weapons)

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = "player_moves/player"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}1.png")


        # Load textures for walking
        self.walk_textures = []
        for i in range(1,5):
            texture = load_texture_pair(f"{main_path}{i}.png")
            self.walk_textures.append(texture)

    def findAngle(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
        self.vector_x = self.mouse_pos_x - SCREEN_WIDTH/2
        self.vector_y = self.mouse_pos_y - SCREEN_HEIGHT/2
        self.weapons.angle = degrees(atan(self.vector_y/self.vector_x))

    #Netušim co se tu děje
    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.weapons.attack == True:
            if self.mouse_pos_x < SCREEN_WIDTH/2 and self.character_face_direction == RIGHT_FACING:
                self.character_face_direction = LEFT_FACING
                self.weapons.face_dir = LEFT_FACING
            elif self.mouse_pos_x > SCREEN_WIDTH/2 and self.character_face_direction == LEFT_FACING:
                self.character_face_direction = RIGHT_FACING
                self.weapons.face_dir = RIGHT_FACING
        else:
            if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
                self.character_face_direction = LEFT_FACING
                self.weapons.face_dir = LEFT_FACING
            elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
                self.character_face_direction = RIGHT_FACING
                self.weapons.face_dir = RIGHT_FACING

        # Idle stand animation
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

        self.shadowCenter = arcade.Sprite("shadowCenter.png", 0.5)  # 15x3
        self.shadowCenter.center_x = self.center_x
        self.shadowCenter.center_y = self.center_y - 19
        self.shadow_list.append(self.shadowCenter)

        self.shadowLeft = arcade.Sprite("shadowSide.png", 0.5)  # 5x3
        self.shadowLeft.center_x = self.shadowCenter.center_x - 13 / 2
        self.shadowLeft.center_y = self.shadowCenter.center_y
        self.shadow_list.append(self.shadowLeft)

        self.shadowRight = arcade.Sprite("shadowSide.png", 0.5)
        self.shadowRight.angle = 180
        self.shadowRight.center_x = self.shadowCenter.center_x + 13 / 2
        self.shadowRight.center_y = self.shadowCenter.center_y
        self.shadow_list.append(self.shadowRight)

        self.shadowTop = arcade.Sprite("shadowTop.png", 0.5)  # 15x2
        self.shadowTop.center_x = self.shadowCenter.center_x
        self.shadowTop.center_y = self.shadowCenter.center_y + 3 / 2
        self.shadow_list.append(self.shadowTop)

        self.shadowBot = arcade.Sprite("shadowTop.png", 0.5)
        self.shadowBot.angle = 180
        self.shadowBot.center_x = self.shadowCenter.center_x
        self.shadowBot.center_y = self.shadowCenter.center_y - 3 / 2
        self.shadow_list.append(self.shadowBot)


    def getShadowCenter(self):
        return [self.shadowCenter.center_x,self.shadowCenter.center_y]

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

        arcade.set_background_color([13,9,9])

        self.tile_list = arcade.SpriteList()
        self.collider_list = arcade.SpriteList()

        self.listLogicalMap = []

        self.creatingGraphicalMapByLogicalMap(self.listLogicalMap)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False


    def creatingGraphicalMapByLogicalMap(self, listLogicalMap): #vykreslení políček

        #přečte z texťáku s mapou písmenka a přepíše je do 2 rozměrného pole
        with open("logical_map_layout_test.txt", 'r') as logicalMap:
            x = TILE_WIDTH//2
            y = TILE_WIDTH//2
            for lineOfLogicalMap in logicalMap:
                self.listLogicalMap.append([])
                for charInLineOfLogicalMap in lineOfLogicalMap:
                    if charInLineOfLogicalMap != "\n":
                        self.listLogicalMap[len(self.listLogicalMap) - 1].append(charInLineOfLogicalMap)

        #projíždí prvky pole a pokud políčko není zobrazeno jako prázdné, tak se vykreslí políčko
        xCounterList = 0
        yCounterList = 0
        for lineOfLogicalMap2 in listLogicalMap:
            for charInLineOfLogicalMap2 in lineOfLogicalMap2:
                if charInLineOfLogicalMap2 != "-":
                    tile = arcade.Sprite("textura_podlaha128.png", 0.5)
                    tile.center_x = x
                    tile.center_y = y
                    self.tile_list.append(tile)

                    #pokud se stane, že políčko vedle právě vykreslovaného je prázdné, tak se správně otočí a zobrazí textura zdi
                                            # ktery CounterList, horni/spodni rada, yCounter check, xCounter check, úhel
                    RotationPossibilities = [[yCounterList, 0, -1, 0,-90],
                                             [xCounterList, 0,  0 , -1,0],
                                             [yCounterList, len(listLogicalMap) - 1, 1, 0,90],
                                             [xCounterList, len(listLogicalMap[0])- 1, 0, 1, 180]]

                    for indexRotationPossibilities in RotationPossibilities:
                        irp = indexRotationPossibilities
                        if irp[0] == irp[1] or listLogicalMap[yCounterList+irp[2]][xCounterList+irp[3]] == "-":
                            tile_wall = arcade.Sprite("textura_zed128.png", 0.5)
                            tile_wall.angle = irp[4]
                            tile_wall.center_x = x
                            tile_wall.center_y = y
                            self.tile_list.append(tile_wall)

                            tile_invisible_barrier = arcade.Sprite("invisible_wall_barrier.png", 0.5)
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

    def set_vsync(self, vsync: bool):
        """ Set if we sync our draws to the monitors vertical sync rate. """
        super().set_vsync(vsync)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()

        self.player = PlayerCharacter()
        self.player.center_x = 32 + TILE_WIDTH
        self.player.center_y = 32 - TILE_WIDTH
        self.player_list.append(self.player)
        self.player.createShadow()
        self.player.weapons.giveWeapon(self.player.center_x, self.player.center_y)


        #self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.collider_list, gravity_constant = 0)


    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        self.tile_list.draw()
        self.collider_list.draw()
        self.player.shadow_list.draw()
        self.player_list.draw()
        self.player.weapon_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        """self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0"""

        #self.physics_engine.update()

        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0




        #print(self.player.center_x, self.player.center_y)

        if self.up_pressed and not self.down_pressed and len(self.player.shadowTop.collides_with_list(self.tile_list)) > 0:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed and len(self.player.shadowBot.collides_with_list(self.tile_list)) > 0:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed and len(self.player.shadowLeft.collides_with_list(self.tile_list)) > 0:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed and len(self.player.shadowRight.collides_with_list(self.tile_list)) > 0:
            self.player.change_x = MOVEMENT_SPEED


        """
        collisionlist = arcade.check_for_collision_with_list(self.shadow_list, self.collider_list)

        if len(collisionlist) > 0:
            self.player.collision_Detected = True
            print("uu")
        else:
            self.player.collision_Detected = False
        """

        self.player_list.update()
        self.player_list.update_animation()
        self.player.weapon_list.update_animation()


        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.


        arcade.set_viewport(self.player.center_x - SCREEN_WIDTH/2,
                            self.player.center_x + SCREEN_WIDTH/2,
                            self.player.center_y - SCREEN_HEIGHT/2,
                            self.player.center_y + SCREEN_HEIGHT/2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.weapons.attack = True
            self.player.findAngle(x, y)




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
