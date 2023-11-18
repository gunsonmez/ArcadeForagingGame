"""
Better Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
This is slightly better than sprite_move_keyboard.py example
in how it works, but also slightly more complex.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard_better
"""

import arcade
import random
import numpy as np
import time


SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_COIN = 0.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"
MOVEMENT_SPEED = 5

MAX_TRIAL = 3
MAX_TIME = 20

CLUSTER_SIZE = 75
CLUSTER_NUMBER = 5
COIN_COUNT = (CLUSTER_NUMBER*CLUSTER_SIZE)+CLUSTER_NUMBER

CONDITION = "Time"

CSV_TITLES = ["Time", "X_Pos", "Y_Pos"]





class Player(arcade.Sprite):

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        #Time
        self.total_time = 0.0

              # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        self.trial = 0

        self.participantNo = random.randint(1,100)*100+random.randint(1,100)

        self.datalist= None

        self.time= 0

    def coin_generate(self):

        parents = CLUSTER_NUMBER
        r = CLUSTER_SIZE
        children = (COIN_COUNT - CLUSTER_NUMBER)//CLUSTER_NUMBER
        parent_point_list = []
        for p in range(parents):
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            point = (x, y)
            parent_point_list.append(point)

        children_point_list = []
        for p in range(parents):
            for c in range(children):
                while True:
                    x = random.randrange(parent_point_list[p][0] - r, parent_point_list[p][0] + r)
                    y = random.randrange(parent_point_list[p][1] - r, parent_point_list[p][1] + r)
                    if 0 < x and x < SCREEN_WIDTH and 0 < y and y < SCREEN_HEIGHT:
                        break
                point = (x, y)
                children_point_list.append(point)

        parent_point_list.extend(children_point_list)
        point_list = parent_point_list

        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)

            # Position the coin

            coin.center_x = point_list[i][0]
            coin.center_y = point_list[i][1]

            # Add the coin to the lists
            self.coin_list.append(coin)


    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        self.total_time = 0.0

        self.time = time.time()

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2
        self.player_list.append(self.player_sprite)

        self.coin_generate()
        self.datalist=[]
        self.trial += 1





    def on_draw(self):
        """ Draw everything """

        # Start timing how long this takes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60


        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 18)

        output = f"Location: {self.player_sprite.center_x}, {self.player_sprite.center_y}"
        arcade.draw_text(output, 10, 35, arcade.color.BLACK, 18)

        # Display timings
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 25, arcade.color.BLACK, 18)

        if self.total_time > MAX_TIME:
            arcade.start_render()
            start_y = SCREEN_HEIGHT / 2
            start_x = SCREEN_WIDTH / 2
            arcade.draw_text("PLEASE WAIT",
                             start_x, start_y, arcade.color.WHITE, 20, width=200, align="center",
                             anchor_x="center", anchor_y="center")

        if self.total_time > MAX_TIME and self.trial == MAX_TRIAL:
            arcade.start_render()
            start_y = SCREEN_HEIGHT / 2
            start_x = SCREEN_WIDTH / 2
            arcade.draw_text("END",
                             start_x, start_y, arcade.color.WHITE, 20, width=200, align="center",
                             anchor_x="center", anchor_y="center")





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

    def on_update(self, delta_time):
        """ Movement and game logic """


        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()


        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


        time_passed = (time.time()-self.time)

        data=(round(time_passed,3), round(self.total_time, 3),round(self.player_sprite.center_x, 2),round(self.player_sprite.center_y, 2))
        self.datalist.append(data)
        self.total_time += delta_time






        """self.total_time += delta_time

        time = round(self.total_time,2)
        player_x = round(self.player_sprite.center_x, 2)
        player_y = round(self.player_sprite.center_y, 2)
        save_data = [time, player_x, player_y]
        data_str = str(save_data)
        file = open(f"player{self.participantNo}trial{self.trial}.txt", "a")
        file.write(data_str)"""

        data_array = np.array(self.datalist)

        np.savetxt(f"ClusteredPlayer{self.participantNo}trial{self.trial}.csv",
                   data_array,
                   delimiter=", ",
                   fmt='% s')


        if self.total_time > MAX_TIME + 5 and self.trial < 3:


            self.setup()





def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()




if __name__ == "__main__":
    main()