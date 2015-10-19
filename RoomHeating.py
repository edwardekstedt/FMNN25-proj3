# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:16:08 2015

@author: Edward
"""
from numpy import *
from mpi4py import MPI
from Laplace import *



class roomHeating(object):
    def __init__(self,dx,w,n):
        ## TODO: CLEAN UP CODE AND MAKE ROOM FOR UPDATING GRID
        self.dx = dx
        self.w = w
        self.n = n
        self.laplIter()
    
    
    def laplIter(self):
        self.largeRoom = self.initlargeroom(self.dx)
        self.smallRoomW = self.initsmallroom(self.dx,'west')
        self.smallRoomE = self.initsmallroom(self.dx,'east')
        self.updateU()
        
    def updateU(self):
        ## TODO: INSERT MPI UPDATING CODE
        U = 1
        
    def initsmallroom(self,dx,dir):
        X = 1
        Y = 1
        
        grid = zeros([X/(dx)+1,Y/(dx)+1])
        grid = self.initbc(grid,'small',dir)
        return grid
    
    def initbc(self,grid,size,direction=None):
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
        
        
    def initlargeroom(self,dx):
        X = 2
        Y = 1
        grid = zeros([X/(dx)+1,Y/(dx)+1])
        grid = self.initbc(grid,'large')
        return grid

