'''
SPRITE GAME
-----------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''

import random
import arcade

# --- Constants ---
BB8_scale = 0.6
trooper_scale = 0.1
trooper_count = 15
SW = 800
SH = 600
SP = 4
LevelTime = 30


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser = arcade.load_sound("game_assets/Sounds/coin.wav")
        self.grounded = False
        self.slowing = False

    def slowdown(self):
        if self.change_x > 0: #or self.change_x < 0:
            self.change_x = self.change_x * 0.9
            if self.change_x < 0.5:
                self.change_x = 0
                self.slowing = False
        if self.change_x < 0: #or self.change_x < 0:
            self.change_x = self.change_x * 0.9
            if self.change_x > -0.5:
                self.change_x = 0
                self.slowing = False

    def update(self):
        global LevelTime
        if self.grounded!=True:
            self.change_y -= (8/60)
        else:
            self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_y > 6:
            self.change_y = 6

        if self.left < 0:
            self.left = 0
            #arcade.play_sound(self.laser)
        elif self.right > SW:
            self.right = SW
            #arcade.play_sound(self.laser)
        if self.top < 0:
            LevelTime = 0
            #arcade.play_sound(self.laser)
        elif self.top > SH:
            self.top = SH
            #arcade.play_sound(self.laser)

        if self.slowing == True:
            if self.grounded == True:
                self.slowdown()




class Trooper(arcade.Sprite):
    def __init__(self):
        self.textureframe = 0
        super().__init__()
        self.w = int(self.width)
        self.h = int(self.height)
        self.angle = 0
        self.scale = 0.2

        #self.draw_hit_box()

        #self.textureframe = 0
        self.texture_list = []
        texture = arcade.load_texture("game_assets/Coins/frame_0.gif")
        self.texture_list.append(texture)
        texture = arcade.load_texture("game_assets/Coins/frame_1.gif")
        self.texture_list.append(texture)
        texture = arcade.load_texture("game_assets/Coins/frame_2.gif")
        self.texture_list.append(texture)
        texture = arcade.load_texture("game_assets/Coins/frame_3.gif")
        self.texture_list.append(texture)
        texture = arcade.load_texture("game_assets/Coins/frame_4.gif")
        self.texture_list.append(texture)
        texture = arcade.load_texture("game_assets/Coins/frame_5.gif")
        self.texture_list.append(texture)
        self.texture = texture


    def update(self):
        self.center_y += -1

    def update_animation(self, delta_time: float = 1/12):
        #print("test")
        self.textureframe += 1
        if self.textureframe > 5:
            self.textureframe = 0
        self.texture = self.texture_list[self.textureframe]

class Backround():
    def __init__(self, speed,x,y,h):
        self.speed = speed
        self.x = x
        self.y = y
        self.inx = x
        self.h = h

    def drawmount(self):
        if self.x > -200 and self.x < 1000:
            arcade.draw_rectangle_filled(self.x,self.y,self.h,self.h,arcade.color.GREEN,45)
            arcade.draw_rectangle_outline(self.x, self.y, self.h, self.h, arcade.color.GRAY,1,45)

    def updatemont(self):
        #self.x += self.speed
        if self.x < -200:
            self.x = random.randint(1000,1200)

class World(arcade.Sprite):
    def __init__(self,texpath):
        self.texturepath = texpath
        super().__init__(self.texturepath, 1)
        self.laser = arcade.load_sound("game_assets/Sounds/coin.wav")

    def update(self):
        pass



#------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self,SW,SH,title):
        self.time = 0
        self.cooldown = 0
        self.ct = 0
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        self.set_vsync(True)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def reset(self):


        #this is the list of the grass blocks
        self.worldlist = arcade.SpriteList() #floor
        for i in range(int(SW / 32)):
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i)
            self.floor.center_y = 80 -16
            self.worldlist.append(self.floor)

        for i in range(int(SW / 32)):
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i)
            self.floor.center_y = 420
            self.worldlist.append(self.floor)

        for i in range(int(SW / 32)):
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i)
            self.floor.center_y = 600
            self.worldlist.append(self.floor)

        for i in range(int(300 / 32)): #lower Platform
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i)
            self.floor.center_y = 200
            self.worldlist.append(self.floor)

        for i in range(int(300 / 32)): #Upper Platform
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i) + 400
            self.floor.center_y = 320
            self.worldlist.append(self.floor)

        for i in range(int(SW / 32)):
            self.floor = World("game_assets/worldtiles/Dirt1.png")
            self.floor.center_x = (32 / 2) + (32 * i)
            self.floor.center_y = 80 -16 -32
            self.worldlist.append(self.floor)

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        self.backlist = []
        for i in range(25):
            background = Backround(-0.5, random.randint(-200, 1000), 0, random.randint(50, 200))
            self.backlist.append(background)

        self.score = 0

        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.center_y = 400
        self.player_list.append(self.BB8)

        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w,SW-trooper.w)
            trooper.center_y = random.randrange(trooper.h+90,SH)
            self.trooper_list.append(trooper)

    def newplat(self):
        print("new plat")
        offset = random.randrange(0,SW-300)
        for i in range(int(300 / 32)): #Upper Platform
            self.floor = World("game_assets/worldtiles/grass.png")
            self.floor.center_x = (32 / 2) + (32 * i) + offset
            self.floor.center_y = SH + 20
            self.worldlist.append(self.floor)

    def newcoin(self):
        print("new coin")
        coin = Trooper()
        coin.center_y = SH + 20
        coin.center_x = random.randrange(10,SW-10)
        self.trooper_list.append(coin)



    def on_draw(self):
        arcade.start_render()

        for obj in self.backlist:
            obj.drawmount()

        self.worldlist.draw()

        self.trooper_list.draw()
        self.player_list.draw()

        arcade.draw_rectangle_filled(SW/2,5,SW,30,arcade.color.BLACK)
        output = f"Score: {self.score}"
        timeremaining = f"Time Left: {LevelTime:.2f}"
        arcade.draw_text(output,10,1, arcade.color.WHITE, 14)
        arcade.draw_text(timeremaining, 100, 1, arcade.color.WHITE, 14)

        if LevelTime <= 0:
            arcade.draw_rectangle_filled(SW/2,SH/2,SW,SH,arcade.color.BLACK)
            arcade.draw_text("Game Over!",SW/2,SH/2,arcade.color.WHITE,30,align= "center",anchor_x="center",anchor_y= "center")

    def on_update(self, dt):
        global LevelTime



        self.time +=1
        if self.time == 4:
            self.time = 0
            self.trooper_list.update_animation()
            LevelTime -= (4 / 60)

        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0

        #self.BB8.angle = - 0.5 * (angle(self.BB8.change_x,self.BB8.change_y+8) + 90)



        self.player_list.update()
        self.trooper_list.update()

        for obj in self.backlist:
            obj.updatemont()
            obj.x = obj.inx - ( 0.1 * self.BB8.center_x)

        trooper_hit_list = arcade.check_for_collision_with_list(self.BB8,self.trooper_list)
        for troop in trooper_hit_list:
            troop.kill()
            self.score +=1
            arcade.play_sound(self.BB8.laser)
            self.newcoin()
            LevelTime += 0.5

        for plat in self.worldlist:
            plat.center_y += -1
            if plat.center_y < -20:
                plat.kill()
                if self.cooldown < 1:
                    self.newplat()
                    self.cooldown += 60

        for coin in self.trooper_list:
            if coin.center_y < -20:
                coin.kill()
                self.newcoin()



        #logic for detecting if player is on the ground
        groundcheck = arcade.check_for_collision_with_list(self.BB8,self.worldlist)
        if self.BB8.change_y < 0.1:
            if groundcheck:
                for obj in groundcheck:
                    if abs(obj.top - self.BB8.bottom) < 7:
                        self.BB8.bottom = obj.top -2

                        self.BB8.grounded = True
            if not groundcheck:
                self.BB8.grounded = False




    def on_key_press(self, symbol, modifiers: int):
        print(symbol)
        # if symbol ==119:
        #     self.BB8.change_y = SP
        #
        # if symbol ==115:
        #     self.BB8.change_y = -SP

        if symbol ==97:
            self.BB8.slowing = False
            self.BB8.change_x = -SP

        if symbol ==100:
            self.BB8.slowing = False
            self.BB8.change_x = SP

        if symbol == 32:
            if self.BB8.grounded == True:
                self.BB8.center_x += 1
                self.BB8.change_y = 6
                self.BB8.grounded = False

    def on_key_release(self, symbol: int, modifiers: int):
        print(symbol)
        # if symbol ==119:
        #     self.BB8.change_y = 0
        #
        # if symbol ==115:
        #     self.BB8.change_y = 0

        if symbol ==97:
            if self.BB8.change_x < 0:
                self.BB8.slowing = True

        if symbol ==100:
            if self.BB8.change_x > 0:
                self.BB8.slowing = True






#-----Main Function--------
def main():
    window = MyGame(SW,SH,"Endless Platforms")
    window.reset()
    arcade.run()

#------Run Main Function-----
if __name__ == "__main__":
    main()