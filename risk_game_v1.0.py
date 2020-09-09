# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:52:13 2020

@author: ilazaar
"""

import numpy as np
import matplotlib.pyplot as plt
import logging, logging.config

#---------------

def drawGrid(grid, interactive, msg):
    '''
    # draw the grid and queens
    # params:
    #       grid: the grid to draw
    #       interactive: if True activate interctive mode with shell, False static draw 
    #       msg: message to show in the title
    '''
    
    extent = [0, grid.shape[0], 0, grid.shape[1]] # axis
    
    palette = np.array([
                    [255,   0,   0],   # red
                    [  255, 255,   255]   # white
                    ])  
    
    RGB = palette[grid]
    
    if(interactive==True):
        plt.ion() # turns interactive mode on with shell
        
    else:
        plt.ioff() # turns interactive mode off with shell
    plt.title(msg)
    plt.imshow(RGB, origin='lower', extent=extent) # draw the grid
    plt.gca().set_xticks(np.arange(0, grid.shape[0], 1))
    plt.gca().set_yticks(np.arange(0, grid.shape[1], 1))
    plt.gca().set_xticklabels(np.arange(0, grid.shape[0], 1))
    plt.gca().set_yticklabels(np.arange(0, grid.shape[1], 1))
    plt.grid(True)
    
    queens_markers = getQueenMarkers() # retrive queens postions to be drawed in grid
    
    for q in queens_markers: # draw queen in the grid
        x, y = zip(*q)
        plt.plot(x, y, '*')
    
    plt.show()

    
def fillQueenTiles(grid, queen_position):
    '''
    # fill queen's tiles in the grid
    # params:
    #       grid: grid to be filled with queen's tiles
    #       queen_position: queen's position in the grid
    # return: 
    #       grid: array filled grid with queen's tiles
    '''
    
    for x in range(grid_size):
        grid[queen_position[1]-1, x]=0
    for y in range(grid_size):
        grid[y, queen_position[0]-1]=0
           
    for i in range(grid_size):
        for j in range(grid_size):
            if(i <= queen_position[1]-1 and j<= queen_position[0]-1 and i==j):
                grid[queen_position[1]-1-i, queen_position[0]-1-j]=0
    
    for i in range(grid_size):
        for j in range(grid_size):
            if(queen_position[1]-1+i < grid_size and queen_position[0]-1+j < grid_size and i==j):
                grid[queen_position[1]-1+i, queen_position[0]-1+j]=0
                
    for i in range(grid_size):
        for j in range(grid_size):
            if(queen_position[1]-1+i < grid_size and queen_position[0]-1-j >= 0 and i==j):
                grid[queen_position[1]-1+i, queen_position[0]-1-j]=0
                
    for i in range(grid_size):
        for j in range(grid_size):
            if(queen_position[1]-1-i >= 0 and queen_position[0]-1+j < grid_size and i==j):
                grid[queen_position[1]-1-i, queen_position[0]-1+j]=0
                
    return grid

def getQueenMarkers():  
    '''
    # get queens markers to be filled in the grid
    # params:
    #       na
    # return: 
    #       queens_markers: list of queens markers
    '''
    queens_markers = []
    
    for q in queens_positions:       
        queens_markers.append([(q[0]-0.5, q[1]-0.5)])
     
    return queens_markers

def checkFreePositions():
    '''
    # check if there is at least one free postion within the grid
    # params:
    #       na
    # return: 
    #       check_free_positions: bool True there is at least one free postion, False no free position
    '''
    check_free_positions = False
    
    if 1 in grid:
        check_free_positions = True

    return check_free_positions

class InputError(Exception):
    '''
    # customized Exception to handel input error
    '''
    pass


#-----------------------------

queens_positions = [] # queens positions
grid = [] # the grid
msg = "" # message to show on grid title


# Logger
logConfigPath = 'C:/Dev/Code/risk/logger/config_v1.0.ini' # path declared in this way to make it easy, but it should be extracted from a config file
logging_config = logging.config.fileConfig(logConfigPath)
logger = logging.getLogger(logging_config)

grid_size_text = input ("Choose your grid size: ")

try:
  grid_size = int(grid_size_text)
  if(grid_size <= 0):
      raise ValueError
      
except ValueError:
  print("Error: not valid input grid size")
else: # if no exception (given grid size is a valid value)
    logger.info('Start New Game ==> Grid size: {0}x{1} - Queen(s): {2}'.format(grid_size, grid_size, grid_size))
    
    grid = np.array([[1]*grid_size for i in range(grid_size)]) # all position are filled with 1, it means the postion is free, 0 not free
    nbQueens = grid_size # number of queens
    i=1
    
    drawGrid(grid, True, "Starting New Game")
    
    while (i <= nbQueens):
        
        while True:
            print ("Give your queen {0} postion within the grid".format(i))
            queen_x_text = input ("enter x: ")
            queen_y_text = input ("enter y: ")
            
            try:
                  queen_x = int(queen_x_text)
                  queen_y = int(queen_y_text)
                  if(queen_x > grid_size or queen_y > grid_size or queen_x <= 0 or queen_y <= 0):
                      raise ValueError
                  if(grid[queen_y-1, queen_x-1] == 0):
                      raise InputError("Not avalaible position") 
                          
            except ValueError:
              print("Error: not valid position input for queen {0}".format(i))
            except InputError :
                print("Choose a free position for queen {0}".format(i))
            else: # if no exception (given queen's position are valid values)
                logger.info('Queen {0} ==> x:{1}, y: {2}'.format(i, queen_x, queen_y))
                new_queen_position = [queen_x, queen_y]
                queens_positions.append(new_queen_position)
                grid = fillQueenTiles(grid, new_queen_position)
                msg = "Enter Queen "+str(i+1)+" position"
                drawGrid(grid, True, msg)
                
                if(checkFreePositions() == False and i < nbQueens): # no free position avalaible in the grid
                    logger.info('End ==> a loss')
                    msg = "You lost ! -> all tiles are red and still "+ str(nbQueens-i) +" to add"
                    print (msg)
                    i = nbQueens+1
                    break
                
                if(i == nbQueens): # all queens were added in the grid
                    logger.info('End ==> a gain')
                    msg = "You win ! -> all queens are on the grid"
                    print (msg)
                    i = nbQueens+1
                    break
                    
                i+=1 # handel next queen to be added on the grid
                break

drawGrid(grid, False, msg)

