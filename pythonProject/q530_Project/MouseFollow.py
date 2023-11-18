import math
import arcade
import random
import numpy as np

CONDITION = 1  # 1=clustered, 2=dispersed

SPRITE_SCALING_PLAYER = 0.4  # Player icon size
SPRITE_SCALING_COIN = 0.2  # Coin icon size

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 3

MAX_TRIAL = 3  # Trial count
MAX_TIME = 20  # How long each trial takes

if CONDITION == 1:
    CLUSTER_R = 75  # Coins will be generated in a 2r*2r square for each cluster
    CLUSTER_N = 75  # Coin number in one cluster, generated around parent coins
    CLUSTER_NUMBER = 5  # Parent coin number, these are randomly generated to define cluster locations
    COIN_COUNT = (CLUSTER_NUMBER * CLUSTER_N) + CLUSTER_NUMBER
    condition_name = "Clustered_MouseFollow"
elif CONDITION == 2:
    COIN_COUNT = 380  # Will be randomly generated from a uniform distribution over the whole field
    condition_name = "Dispersed_MouseFollow"

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

        # Score
        self.score = 0

        # Time
        self.total_time = 0.0

        # Trial
        self.trial = 0

        # Player data
        self.datalist = None

        # Mouse cursor visible
        self.set_mouse_visible(True)

        # Generate random player number # Not the best way, will change in the future
        self.participantNo = random.randint(1, 10000)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def coin_generate(self):  # Coin generation function : Dispersed or clustered distributions

        if CONDITION == 1:
            parents = CLUSTER_NUMBER
            r = CLUSTER_R
            children = CLUSTER_N
            parent_point_list = []
            for p in range(parents):  # Cluster Locations generated from uniform distribution
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(SCREEN_HEIGHT)
                point = (x, y)
                parent_point_list.append(point)

            children_point_list = []
            for p in range(parents):  # For every cluster
                for c in range(children):  # Generate coins from uniform distribution
                    while True:  # In the 2r*2r square around the parent coins
                        x = random.randrange(parent_point_list[p][0] - r, parent_point_list[p][0] + r)
                        y = random.randrange(parent_point_list[p][1] - r, parent_point_list[p][1] + r)
                        if 0 < x and x < SCREEN_WIDTH and 0 < y and y < SCREEN_HEIGHT:
                            break
                    point = (x, y)
                    children_point_list.append(point)

            parent_point_list.extend(children_point_list)
            point_list = parent_point_list
        elif CONDITION == 2:
            point_list = []
            for c in range(COIN_COUNT):
                x = random.randrange(SCREEN_WIDTH)
                y = random.randrange(SCREEN_HEIGHT)
                point = (x, y)
                point_list.append(point)

        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = point_list[i][0]
            coin.center_y = point_list[i][1]

            # Add the coin to the list
            self.coin_list.append(coin)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Initialize score
        self.score = 0

        # Initialize time
        self.total_time = 0.0

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

        # Generate coins
        self.coin_generate()

        # Initialize datalist
        self.datalist = []

        # Add to the trial count before starting a new trial
        self.trial += 1

    def on_draw(self):
        """ Draw everything """

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        arcade.start_render()  # Render starts the drawing phase, needed for every scene change
        self.coin_list.draw()
        self.player_list.draw()

        # Display score
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 18)

        # Display location
        output = f"Location: {round(self.player_sprite.center_x)}, {round(self.player_sprite.center_y)}"
        arcade.draw_text(output, 10, 35, arcade.color.BLACK, 18)

        # Display time
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 25, arcade.color.BLACK, 18)

        # If trial time is exceeded, proceed to a break screen
        if self.total_time > MAX_TIME:
            arcade.start_render()
            start_y = SCREEN_HEIGHT / 2
            start_x = SCREEN_WIDTH / 2
            arcade.draw_text("PLEASE WAIT",
                             start_x, start_y, arcade.color.WHITE, 20, width=200, align="center",
                             anchor_x="center", anchor_y="center")

        # If the trials are over, proceed to an end screen
        if self.total_time > MAX_TIME and self.trial == MAX_TRIAL:
            arcade.start_render()
            start_y = SCREEN_HEIGHT / 2
            start_x = SCREEN_WIDTH / 2
            arcade.draw_text("END",
                             start_x, start_y, arcade.color.WHITE, 20, width=200, align="center",
                             anchor_x="center", anchor_y="center")

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y

        # Get the destination location for the bullet
        dest_x = x
        dest_y = y

        # Do the math to calculate how to get to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle player will move forward to.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # One unit movement in the direction of the target (cursor)
        self.player_sprite.change_x = math.cos(angle) * MOVEMENT_SPEED
        self.player_sprite.change_y = math.sin(angle) * MOVEMENT_SPEED

    def on_update(self, delta_time):
        """ Movement and game logic """

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

        # Saving time and location data every new frame
        data = (round(self.total_time, 3), round(self.player_sprite.center_x, 2), round(self.player_sprite.center_y, 2))
        self.datalist.append(data)
        self.total_time += delta_time

        data_array = np.array(self.datalist)

        # Save data as .csv
        np.savetxt(f"{condition_name}Player{self.participantNo}trial{self.trial}.csv",
                   data_array,
                   delimiter=", ",
                   fmt='% s')
        # Save data as .npy
        np.save(f"{condition_name}Player{self.participantNo}trial{self.trial}", data_array)

        # If time limit is exceeded (trial_time + break_time) start a new trial
        if self.total_time > MAX_TIME + 5 and self.trial < MAX_TRIAL:
            self.setup()



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, condition_name)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
