# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:16:08 2015

@author: Edward
"""
from numpy import *
from mpi4py import MPI
from Laplace import *



class roomHeating(object):
    def __init__(self,dx):
        ## TODO: CLEAN UP CODE AND MAKE ROOM FOR UPDATING GRID
        self.dx = dx
        self.largeRoom = self.initRoom(self.dx,'large')
        self.smallRoomW = self.initRoom(self.dx,'small','west')
        self.smallRoomE = self.initRoom(self.dx,'small','east')
        self.solver = laplaceSolver(dx)
    def __call__(self,w,n):
        self.w = w
        self.n = n
        self.updateU()


    def updateU(self):
        ## TODO: INSERT MPI UPDATING CODE
        for i in range(self.n):
            lrOld = self.largeRoom.copy()
            self.largeRoom = self.solver(self.largeRoom,'Dirichlet')
            self.largeRoom = self.w*self.largeRoom +(1-self.w)*lrOld
            
            
       
        
    def initRoom(self,dx,size,dir=None):
        if size == 'small':
            X = 1
            Y = 1  
        elif size == 'large':
            X = 2
            Y = 1
        else:
            raise NameError('size must be "small" or "large"')
        grid = zeros([X/(dx)+1,Y/(dx)+1])
        grid = self._initbc(grid,size,dir)
        return grid

        
    
    def _initbc(self,grid,size,dir=None):
        gH = 40
        gW = 5
        gN = 15
        if size == 'small':
            if dir == 'west':
                grid[:,0] = gH
            elif dir == 'east':
                grid[:,-1] = gH
            grid[0,:] = gN
            grid[-1,:] = gN
        else:
            grid[0,:] = gW
            grid[-1,:] = gH
            grid[0:(len(grid)-1)/2,0] = gN
            grid[(len(grid)-1)/2:,-1] = gN
        return grid
        
X = roomHeating(1/3.)
X(0.8,5)
      