import pygame
import os
# initialize the font text library
pygame.font.init()
# initialize the sound effects library
pygame.mixer.init()

# create a main surface, can be referred as main window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# name of the window
pygame.display.set_caption("My First Multiplayer Game")

# this will be a line draw as a rect in the middle of the screen
CENTER_BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

# Load in the mixer sound effects
# the gun is for shoot and the grenade is for collide
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
YELLOW_GREEN = (200,255,0)

# defining an FPS. How quickly my main loop will run
FPS = 60

# Bullets set up
BULLET_VEL = 8
BULLET_WIDTH, BULLET_HEIGHT = 12, 6
MAX_BULLETS = 3

# Collide hit event. Create 2 different events
YELLOW_HIT_RED = pygame.USEREVENT + 1
RED_HIT_YELLOW = pygame.USEREVENT + 2

# Players set up
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55,40)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

# SET AND ROTATE THE PLAYERS IMGS - add (os.path.join("assets", "file")) for the folder
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.image.load(
        os.path.join('assets','spaceship_yellow.png')), 90)
RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.image.load(
        os.path.join('assets','spaceship_red.png')), 270)
# RESIZE THOSE PLAYERS IMGS
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Load in the Space Background
SPACE_BACKGROUND = pygame.transform.scale(
    pygame.image.load(
        os.path.join('assets','space.png')), (WIDTH, HEIGHT))

# takes as argument whatever I wanna draw
def draw_window(yellow, red, yellow_bullets, red_bullets, winner_text, yellow_health, red_health):
    # put the fill background here
    # draw things inside that win, background. The drawings is good to do outside the main loop
    #WIN.fill(WHITE)
    WIN.blit(SPACE_BACKGROUND, (0,0))
    # draw the center border, this will not be with blit
    # pygame.draw.rect(where, color, what are we drawing)
    pygame.draw.rect(WIN, BLACK, CENTER_BORDER)    
    # drawing the players. We use blit to draw surfaces to the window
    # and instead of giving then a position, we're going to give them the rect position
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    # put the font to the screen
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10,10))
    
    # the reason I'm not drawing the text winner here, is because
    # I wanna pause the game, run the text for 5 seconds, and then 
    # start the game again

    # draw the bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_GREEN, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # to the drawings work, we need to update the display
    pygame.display.update()

def draw_winner(winner_text):
    winner_draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(winner_draw_text, (CENTER_BORDER.x - winner_draw_text.get_width()/2, HEIGHT/2 - winner_draw_text.get_height()))
    pygame.display.update()
    # pause the game
    pygame.time.delay(5000)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < CENTER_BORDER.x: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > CENTER_BORDER.x + CENTER_BORDER.width: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # move the bullets, handle the collision of the bullets, and removing them when off the screen
    # loop through all the yellow_bullets, see if they collide or go off and do the same for the red
    for bullet in yellow_bullets:
        # start moving them, to the right
        bullet.x += BULLET_VEL
        # after we move, we're gonna check for collision, if the red player collided with the bullet
        if red.colliderect(bullet):
            # if collide, remove bullet
            # but also, we need to informe the main loop that red has been shoot
            # we're going to post an event!
            print('event')
            pygame.event.post(pygame.event.Event(YELLOW_HIT_RED))
            yellow_bullets.remove(bullet)
        # now, check if the bullets go off the screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT_YELLOW))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# main game loop. Collisions, logics, etc
def main():
    # draw 2 rectangles to move them as players
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(600, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    # define another key that the players can press to shoot a bullet
    # first, let's define an empty list
    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10
    
    # define a clock object
    clock = pygame.time.Clock()
    # while loop will be an infinite loop
    run = True
    while run:
        # set the FPS for the game's clock
        clock.tick(FPS)
        # giving us a list with all the events and we're looping through them
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # when run = False, quit the game
                #pygame.quit()
            
            # another way to look up for keys pressed, once x time
            if event.type == pygame.KEYDOWN:
                # create/fire a bullet. left-control for yellow
                """ 
                bullet will be just a rect, placed wherever the player is
                as yellow shoot for the right, the bullet needs to be created 
                at the right position of the ship, the x plus the width
                the y position will be in the middle of the ship, so
                the height/2, minus the half height of the bullet
                as we can not have float numbers, we add // when dividing
                """
                # wherever we fire a bullet, create also a sound for it
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:                    
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, 
                        yellow.y + yellow.height//2 - BULLET_HEIGHT//2,
                        BULLET_WIDTH, 
                        BULLET_HEIGHT
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # create/fire a bullet. right-control for red
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, 
                        red.y + red.height//2 - BULLET_HEIGHT//2,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # if ships got hit
            # also play the hit sounds
            if event.type == YELLOW_HIT_RED:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT_YELLOW:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
            winner_text = ""
            if yellow_health <= 0:
                winner_text = "Red Wins!"
            
            if red_health <= 0:
                winner_text = "Yellow Wins!"
            
            if winner_text != "":
                # display text            
                draw_winner(winner_text)
                # and then we will break the while
                # when we break, it will send us to the pygame.quit() or for the new game again with main()
                main()

        # testing the bullets
        #print(yellow_bullets, red_bullets)           

        # as example, for each loop, move my rectangles
        #yellow.x += 1
        keys_pressed = pygame.key.get_pressed()
        # write the keys pressed in a function
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # move the bullets and see if they collide with the characters
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
                
        # calling the draw function, passing the rectangles
        draw_window(yellow, red, yellow_bullets, red_bullets, winner_text, yellow_health, red_health)
    
    pygame.quit()

"""
we'll just run this main funtion when we run this file
if I've imported this file in another file, that function 
will not run until I run the main.py file
"""
if __name__ == "__main__":
    main()