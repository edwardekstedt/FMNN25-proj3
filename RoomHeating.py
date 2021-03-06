# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:16:08 2015

@author: Edward
"""

import numpy as np
from Laplace import *
import matplotlib.pyplot as plt


class roomHeating(object):
    def __init__(self,dx,rank=None,gH = 40,gN =15, gW = 5):
        self.gH = gH
        self.gN = gN
        self.gW = gW
        self.dx = dx
        self.rank = rank
        ## TODO: CLEAN UP CODE
        if rank == 0:
            self.largeRoom = self.initRoom(self.dx,'large')
        elif rank == 1:
            self.smallRoomW = self.initRoom(self.dx,'small','west')
        elif rank == 2:
            self.smallRoomE = self.initRoom(self.dx,'small','east')
        else:
            self.largeRoom = self.initRoom(self.dx,'large')
            self.smallRoomW = self.initRoom(self.dx,'small','west')
            self.smallRoomE = self.initRoom(self.dx,'small','east')
        self.solver = laplaceSolver(dx)
        
        
    def __call__(self,bc = None):
        self.bc = bc
        self.updateU()
        #self.plot()
        if self.rank == 0:
            return self.largeRoom
        if self.rank == 1:
            return self.smallRoomW
        if self.rank == 2:
            return self.smallRoomE
    def updateU(self):
        ## TODO
        if self.rank == 0:
            if self.bc is not None:
                self.largeRoom = self.bc
            self.largeRoom = self.solver(self.largeRoom,'Dirichlet')
        elif self.rank == 1:
            if self.bc is not None:
                self.smallRoomW  = self.bc
            self.smallRoomW = self.solver(self.smallRoomW, 'Neumann','east')
        elif self.rank ==2:
            if self.bc is not None:
                self.smallRoomE = self.bc
            self.smallRoomE = self.solver(self.smallRoomE,'Neumann','west')
    
    def smoothing(self,room,roomOld):
        return self.w*room+(1-self.w)*roomOld
        
    def setRoom(self,loc,room):
        if loc == 'Large':
            self.largeRoom = room
        elif loc == 'SmallE':
            self.smallRoomE = room
        elif loc == 'SmallW':
            self.smallRoomW = room
        else:
            raise NameError('Roomtype does not exist, use Large, SmallE or SmallW')
    
    def getRoom(self,loc):
        if loc == 'Large':
            return self.largeRoom
        elif loc == 'SmallE':
            return self.smallRoomE
        elif loc == 'SmallW':
            return self.smallRoomW
        else:
            raise NameError('Roomtype does not exist, use Large, SmallE or SmallW')
    
    def plot(self):
        plt.figure()
        pM = self.plotMatrix()
        plt.close('all')
        plt.imshow(pM)
        plt.colorbar()
        plt.show()
        
        
    def plotMatrix(self):
        dim1,dim2 = self.smallRoomE.shape
        dim1 = dim1-1
        emptySpace= np.zeros([dim1,dim2])
        emptySpace[:,:] = None
        emptySpace[:,0] = 15
        self.smallRoomE = np.vstack([self.smallRoomE,emptySpace])
        emptySpace = np.fliplr(emptySpace)
        self.smallRoomW = np.vstack([emptySpace,self.smallRoomW])
        plotRoom= np.hstack([self.smallRoomW,self.largeRoom[:,1:-1],self.smallRoomE])
        return plotRoom

    
    def initRoom(self,dx,size,dir=None):
        if size == 'small':
            X = 1
            Y = 1  
        elif size == 'large':
            X = 2
            Y = 1
        else:
            raise NameError('size must be "small" or "large"')
        grid = np.zeros([X/(dx)+1,Y/(dx)+1])
        grid = self._initbc(grid,size,dir)
        return grid

        
    
    def _initbc(self,grid,size,dir=None):
        if size == 'small':
            grid[0,:] = self.gN
            grid[-1,:] = self.gN
            grid[:,-1] = self.gN
            grid[:,0] = self.gH
            if dir == 'west':
                return grid
            elif dir == 'east':
                grid = np.fliplr(grid)
                return grid
        else:
            grid[:,0]=self.gN
            grid[: ,-1] = self.gN
            grid[0,:] = self.gH
            grid[-1,:] = self.gW
            return grid
        