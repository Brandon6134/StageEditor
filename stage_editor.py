import pygame
import button
import csv #allows us to read and write the level_data files ,e.g. files with huge lists of 0,3, 4, -1, 14, etc corresponding to our tile numbers
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21 #we have 21 diff types of tiles that load in game
level = 0
current_tile = 0

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

error_text = False #if load data error has occured

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200,25,25)

font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS #we treat -1 as the value for an empty tile, so we create a row/list of 150 -1's (our screen length)
    world_data.append(r)#add that row/list to a bigger list, so after all loops we have 16 rows of those 150 -1 values to fill our entire screen

#create ground at bottom of screen
#accesses the last row in the world_data list and changes all their values to 0 since 0 value is ground
for tile in range(0,MAX_COLS):
    world_data[ROWS - 1][tile]=0

#load images
pine1_img = pygame.image.load('./img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('./img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('./img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('./img/Background/sky_cloud.png').convert_alpha()
save_img = pygame.image.load('./img/save_btn.png').convert_alpha()
load_img = pygame.image.load('./img/load_btn.png').convert_alpha()

#store tiles in list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.transform.scale(pygame.image.load(f'./img/tile/{x}.png'), (TILE_SIZE, TILE_SIZE))#each of the tile pics r just called 0.png, 1.png, etc
    img_list.append(img)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)#have to take the text, convert to image, then blit that img on screen
	screen.blit(img, (x, y))

def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, ((x*width)-scroll * 0.5,0))
        #set x coordinate blit to  (x*width), so image is blitted one image width after/to the right of the previous image loop.
        #-scroll is so that the image moves left or right when user scrolls
        screen.blit(mountain_img, ((x*width)-scroll*0.6,SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x*width)-scroll*0.7,SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x*width)-scroll*0.8,SCREEN_HEIGHT - pine2_img.get_height()))
        #the *0.5,0.6, etc for scroll are to control the scroll speeds, so here scrolling at different speeds adds a 3D like effect

def draw_grid():
    #draw vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (TILE_SIZE * c - scroll, 0), (TILE_SIZE * c - scroll, SCREEN_HEIGHT))

    #draw horizontal lines    
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0,TILE_SIZE * c), (SCREEN_WIDTH, TILE_SIZE * c))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):#we gain the x and y coordinates of what tile we r dealing with from the enumerate
            if tile >= 0: #only want to draw something if there isn't a -1 value (empty)
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y*TILE_SIZE))#tile is the value for that tile e.g. 3, 5, 18
    
#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200 , SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

#create buttons, this uses a prebuilt button() class from button.py
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1 #counter that moves the buttons created for tile_button, so they aren't overlapping
    #e.g. first button is 75*0 + 50 pixels for x axis, then second is 75*1 + 50 pixels on x axis, etc.
    if button_col == 3: #basically we have 3 buttons per row, then we go to next row
        button_row += 1
        button_col = 0

run = True
while run:
    clock.tick(fps)#controls framerate

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN -90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN -60)

    #save and load data
    if save_button.draw(screen):#if clicked
        #save level data

        #below is pickle method
        pickle_out = open(f'level{level}_data', 'wb')# 'wb' opens file and allows us to write
        pickle.dump(world_data,pickle_out)
        pickle_out.close()

        #below is csv method
        """
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile: # the 'w' allows us to write and open the file?
            writer = csv.writer(csvfile, delimiter = ',')#delimiter is what seperates each of the values that are written to the csv file, in our case a comma
            for row in world_data:#need to add data to the writer row by row
                writer.writerow(row)
        """
    if load_button.draw(screen):
        #reset scroll to start of level
        scroll = 0

        #load in level data

        #below is pickle method
        if path.exists(f'level{level}_data'):
            world_data=[]#empty our world_data to prepare for loading in new data_file
            pickle_in = open(f'level{level}_data', 'rb') #'rb' since we're reading the file
            world_data = pickle.load(pickle_in)
            error_text = False
        else:
            error_text = True
        #below is csv method
        """
        with open(f'level{level}_data.csv', newline='') as csvfile: # no 'w' cus we are just reading file
            reader = csv.reader(csvfile, delimiter = ',')
            for x,row in enumerate(reader):#when reading the file, everything is returned as a string; so we have to go one value at a time and convert each into an int
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        """

    if error_text:
        draw_text(f'Level data could not be found', font, RED, 10, SCREEN_HEIGHT + LOWER_MARGIN -30)

    #draw tile panel and grid on right
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH,0,SIDE_MARGIN, SCREEN_HEIGHT))

    #draw each tile and make them press them
    
    button_count = 0
    for button_count, i in enumerate(button_list): # what enumerate does is that our variable button_count keeps track of which button we're on during the for loop
        if i.draw(screen):
            current_tile = button_count #save current_tile to the index number of selected item/button
    #highlight the selected tile
    pygame.draw.rect(screen,RED,button_list[current_tile].rect,3)#3 is borderline of rectangle
    

    #scroll the map
    if scroll_left and scroll > 0: #scroll > 0 makes sure they don't scroll past our image backgrounds
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH: # second statement makes sure we don't scroll past our backround on the right side
        scroll += 5 * scroll_speed

    #add new tiles to screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE #by dividing by TILE_SIZE, tells us which tile we're in
    #e.g. since tile_size is = 40, if our mouse is in position of 170, then 170//40 = 4 so we're in the 4th tile in x-axis
    y  = pos[1] // TILE_SIZE
    #check if mouse coordinates are within tile area and not in the side margins
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:#remember mouse.get_pressed()[0] refers to left click and returns 1 if down
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:#mouse.get_pressed()[2] refers to right click, as [1] refers to middle mouse click
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5
            
        #release key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()
