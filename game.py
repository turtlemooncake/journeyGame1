# Victoria Li vml8gj

'''
Checkpoint 1:
My game will be an adventure game loosely based on the Legend of Zelda series. There will be two levels,
and the goal is to defeat the Final Boss at the end of the last level. The player will control a sprite that
is navigating through each level. After the first level, the player gets stronger.
The optional features that will be checked off in this game are: animation, enemies, multiple levels,
and scrolling level.

NOTE: This game has two levels and no restart function.
Image url for guy: https://i.stack.imgur.com/gZ3c5.png
I cropped it into two (left moving, right moving).
'''

import gamebox
import pygame

camera = gamebox.Camera(800, 600)

# time
time = 0

# scrollspeed
scrollspeed = 3

# going home
going_home = False

# defeated
defeated = False

'''
Lvl 1 Background
Creation of the first level's scenery. 
'''
# background setup
ground = gamebox.from_color(0, 575, 'peru', 5000, 100)
mountain1 = gamebox.from_image(0, 0, 'mountain1.png')
mountain1.scale_by(.55)
mountain2 = gamebox.from_image(0, 0, 'mountain2.png')
mountain2.scale_by(.55)


# background positions
ground.right = camera.right
ground.left = camera.left
mountain1.bottom = camera.bottom
mountain1.left = camera.left
mountain2.bottom = ground.top
mountain2.left = mountain1.right

background1 = [mountain1, mountain2, ground]

'''
Guy Animation + Movement 
Draws both right and left guys, as well as controls their movement. They can only move forward.
In addition, if a guy touches a mask or a portal, it activates each following function. 
'''
# guy
guy_right = gamebox.load_sprite_sheet('guy_right.png', 1, 4)  # one row, 4 cols; collection of images
animate_right = []
guy_left = gamebox.load_sprite_sheet('guy_left.png', 1, 4)
animate_left = []

# guy bool + global guy
guy_travel_right = False
guy_travel_left = False
guy_x = 0
guy_y = 0


# guy right animation chain
def guy_draw_right():
    global guy_x
    global guy_travel_right
    if guy_travel_right == False:
        for image in guy_right:
            dude = gamebox.from_image(0, 0, image)
            if guy_x != 0:
                    dude.left = guy_x
            else:
                dude.left = camera.left + 100
            dude.bottom = ground.top + 10
            animate_right.append(dude)

# guy lieft animation chain
def guy_draw_left():
    global guy_travel_left, guy_x
    if guy_travel_left == False:
        for image in guy_left:
            dude = gamebox.from_image(0, 0, image)
            if guy_x != 0:
                dude.right = guy_x
            else:
                dude.right = camera.right - 100
            dude.bottom = ground.top + 10
            animate_left.append(dude)


# move animate_right
def guy_move_right():
    global guy_x, guy_y, going_home
    for dude in animate_right:
        dude.move(5, 0)
        dude.speedx = 5
    guy = animate_right[(time // 5) % len(animate_right)]
    guy_x = guy.x
    guy_y = guy.y
    if guy.touches(mask):
        going_home = True
    camera.draw(guy)

# move animate_left
def guy_move_left():
    global guy_x, guy_y, endgame
    for dude in animate_left:
        dude.move(-5, 0)
        dude.speedx = 5
    guy = animate_left[(time // 5) % len(animate_left)]
    guy_x = guy.x
    guy_y = guy.y
    if guy.touches(portal):
        endgame = True
    camera.draw(guy)


'''
Firespells. The key is to keep each fire spell moving with the same x and y position the guy is in. 
Both draws and moves the fire spells. 
'''
fireball = gamebox.from_image(0, 0, 'fireball.png')
fireball.scale_by(0.2)
fireball.flip()

firewall = gamebox.from_image(0, 0, 'fireshield.png')
firewall.scale_by(0.2)

def fire():
    global guy_x, guy_y
    fireball.x = guy_x - 20 # because the guy is moving left here
    fireball.y = guy_y
    fireball.speedx -= 7
    fireball.move_speed()
    camera.draw(fireball)

def fireshield():
    global guy_x, guy_y
    firewall.x = guy_x + 30 # positive because the guy is moving right here
    firewall.y = guy_y
    camera.draw(firewall)

'''
Minions. Two sets to be precise; the level 1 minion and the level 2 minion.
Both are essentially the same except for design and movement direction. The key here was to use the
move.() method instead of the object.x one because that way the minion can still move across the screen.
'''
minions = gamebox.load_sprite_sheet('minions.png', 1, 6)
minions_left = []

def minions_draw():
    for each in minions:
        min = gamebox.from_image(800, 0, each)
        min.scale_by(0.4)
        min.bottom = ground.top
        minions_left.append(min)

def minions_move():
    global animate_right, firewall, defeated
    for every in minions_left:
        every.move(-5, 0)
        every.speedx = scrollspeed + 3
        if every.left_touches(firewall):
            every.move(800, 0)
        if every.right < camera.left:
            every.move(800, 0)
    minion = minions_left[(time // 4) % len(minions_left)]
    if minion.right < camera.left:
        minion.move(800, 0)
    if minion.left_touches(animate_right[0] or animate_right[1] or animate_right[2] or animate_right[3]):
        defeated_by_m()
        defeated = True
    camera.draw(minion)

minions2 = gamebox.load_sprite_sheet('minion2.png', 1, 6)
minions_flipped = []
def minions_draw_flipped():
    for each in minions2:
        min = gamebox.from_image(0, 0, each)
        min.scale_by(0.4)
        min.bottom = ground.top
        minions_flipped.append(min)

def minions_move_left():
    global animate_left, fireball, defeated
    for every in minions_flipped:
        every.move(5, 0)
        every.speedx = scrollspeed + 3
        if every.right_touches(fireball):
            every.move(-800, 0) # took me a while to figure out that -800 would be: take 800 steps to the left
        if every.x > camera.right:
            every.move(-800, 0)
    minion = minions_flipped[(time // 4) % len(minions_flipped)]
    if minion.x > camera.right:
        minion.move(-800, 0)
    if minion.right_touches(animate_left[0] or animate_left[1] or animate_left[2] or animate_left[3]):
        defeated_by_m()
        defeated = True
    camera.draw(minion)

'''
Defeated Screen. 
Shows up when a minion touches the guy. gamebox.pause() is used to freeze the background animation. 
'''
def defeated_by_m():
    global defeated
    if defeated:
        camera.clear('paleturquoise')
        defeat = gamebox.from_image(0, 0, 'defeated.png')
        defeat.center = camera.center
        camera.draw(defeat)
        gamebox.pause()


'''
Start Screen.
First screen that pops up. Essentially a transition scene ot the next one. 
'''
screendone = False
start = False
def start_screen(keys):
    global screendone, start
    camera.clear('cadet blue')
    screen1 = gamebox.from_image(0, 0, 'Screen1.png')
    screen1.center = camera.center
    screen2 = gamebox.from_image(0, 0, 'StarScreen2.png')
    screen2.center = camera.center
    if screendone != True:
        camera.draw(screen1)
    if pygame.K_b in keys:
        screendone = True
    if screendone:
        camera.draw(screen2)
    if pygame.K_g in keys:
        start = True

'''
Mask.
Placed at the end of level 1. Acts as a transition catalyst to level 2. Is drawn in the main tick function. Interacts
with the guy. 
'''
mask = gamebox.from_image(0, 0, 'mask.png')
mask.scale_by(0.2)
mask.x = mountain2.right + 50
mask.bottom = ground.top


'''
Level 1 Movement.
Controls all of level one movement (guy, minion, fireshield). 
'''
def lvl_one(keys):
    global time, guy_travel_right, guy_x, fireball, start
    camera.clear('cadet blue')
    guy_draw_right()
    camera.draw(mask)
    for each in background1:
        camera.draw(each)
    minions_draw()
    minions_move()
    if pygame.K_d in keys:
        guy_move_right()
        guy_travel_right = True
    else:
        guy_travel_right = False
        standing_guy = animate_right[0] # so that it looks like he is standing still when he is not moving
        standing_guy.x = guy_x
        standing_guy.speedx = scrollspeed # key here: so the guy appears to be "standing still"
        camera.draw(standing_guy)
    if pygame.K_s in keys and guy_travel_right == False:
        fireshield()
    camera.x += scrollspeed # positive because he is moving right


'''
Level 2 Transition.
Transition screen after guy touches mask. This is the in-between stop between level 1 and level 2.
'''
lvl_two_go = False
def lvl2_startscreen(keys):
    global lvl_two_go
    camera.clear('cadet blue')
    lvl2_Screen = gamebox.from_image(0, 0, 'Screenlvl2.png')
    lvl2_Screen.center = camera.center
    camera.draw(lvl2_Screen)
    if pygame.K_h in keys:
        lvl_two_go = True

'''
Level 2 Setup.
Background creation for level 2. 
'''

tree1 = gamebox.from_image(0, 0, 'forest1.png')
tree1.scale_by(0.55)
tree2 = gamebox.from_image(0, 0, 'forest2.png')
tree2.scale_by(0.55)
ground_extended = gamebox.from_color(0, 575, 'firebrick', 10000, 100)

# background positions
tree1.bottom = camera.bottom
tree1.left = camera.left
tree2.bottom = camera.bottom
tree2.left = tree1.right
ground_extended.right = ground.left

background2 = [tree2, tree1, ground, ground_extended]

'''
Game End Portal
Catalyst at the end of level 2 for ending the game. 
'''
endgame = False
portal = gamebox.from_image(0, 0, 'endportal.png')
portal.scale_by(0.4)
portal.x = ground_extended.right - 30
portal.bottom = ground_extended.top

'''
Level 2 Movement
Controls all the movement in level 2 (guy left, minions left, fireball)
'''
def lvl_two(keys):
    global background2, guy_travel_left
    camera.clear('mediumslateblue')
    guy_draw_left()
    camera.draw(portal)
    for each in background2:
        camera.draw(each)
    minions_draw_flipped()
    minions_move_left()
    if pygame.K_a in keys:
        guy_move_left()
        guy_travel_left = True
    else:
        guy_travel_left = False
        standing_guy = animate_left[0] # so that he looks like he is standing still when not moving
        standing_guy.x = guy_x
        standing_guy.speedx = -scrollspeed # moving left
        camera.draw(standing_guy)
    if pygame.K_SPACE in keys and guy_travel_left == False:
        fire()
    else:
        fireball.speedx = 0
        fireball.x = guy_x
    camera.x -= scrollspeed # so that the scroll is moving right instad of left


'''
End Screen
The last screen that pops up. At the very end of level 2. 
'''
def endscreen():
    global endgame
    camera.clear('cadet blue')
    last_screen = gamebox.from_image(0, 0, 'lastscreen.png')
    last_screen.center = camera.center
    camera.draw(last_screen)

'''
Main Tick Function
Controls both level 1 and level 2 controller functions. Evaluates booleans to decide when to move on 
to the next level, and when to end the game. 
'''
def tick(keys):
    global time, guy_travel_right, guy_x, fireball, start, lvl_two_go, endgame
    start_screen(keys)
    if start == True and going_home == False:
        lvl_one(keys)
    elif going_home and endgame == False:
        lvl2_startscreen(keys)
        if lvl_two_go:
            lvl_two(keys)
    if endgame:
        endscreen()
    time += 1
    camera.display()

gamebox.timer_loop(30, tick)