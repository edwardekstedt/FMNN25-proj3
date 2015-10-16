# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:16:08 2015

@author: Edward
"""
from numpy import *
from Laplace import *



def main(dx):
    ## TODO: CLEAN UP CODE AND MAKE ROOM FOR UPDATING GRID
    largeroom(dx)

def smallroom(dx):
    X = 1
    Y = 1
    
    grid = zeros([X/(dx)+1,Y/(dx)+1])
    grid = initbc(grid,'west','small')
    print(grid)

def initbc(grid,size,direction=None):
    if size == 'small':
        if direction == 'west':
            grid[:,0] = 40
        elif direction == 'east':
            grid[:,-1] = 40
        grid[0,:] = 15
        grid[-1,:] = 15
    else:
        grid[0,:] = 5
        grid[-1,:] = 40
        grid[0:(len(grid)-1)/2,0] = 15
        grid[(len(grid)-1)/2:,-1] = 15
    return grid
    
    
def largeroom(dx):
    X = 2
    Y = 1
    grid = zeros([X/(dx)+1,Y/(dx)+1])
    grid = initbc(grid,'large')
    print(grid)
    u = Laplace.laplaceSolver(grid,dx)
    U = u('Dirichlet')
    print(U)
main(1/3.)