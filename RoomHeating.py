# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:16:08 2015

@author: Edward
"""
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
from mpi4py import MPI
from Laplace import *
import matplotlib.pyplot as plt
from matplotlib import cm

class roomHeating(object):
    def __init__(self,dx,rank=None):
        ## TODO: CLEAN UP CODE
        if rank == 0:
            self.largeRoom = self.initRoom(self.dx,'large')
        elif rank == 1:
            self.smallRoomW = self.initRoom(self.dx,'small','west')
        elif rank == 2:
        self.dx = dx
        else:
        self.largeRoom = self.initRoom(self.dx,'large')
        self.smallRoomW = self.initRoom(self.dx,'small','west')
        self.smallRoomE = self.initRoom(self.dx,'small','east')
        self.solver = laplaceSolver(dx)
        
        
    def __call__(self,room,bc = None):
        self.room = room
        self.bc = bc
        self.updateU()
        #self.plot()
        if self.room == 'Large':
            return self.largeRoom
        if self.room == 'SmallW':
            return self.smallRoomW
        if self.room == 'SmallE':
            return self.smallRoomE
    def updateU(self):
        ## TODO
        if self.room == 'Large':
            if self.bc != None:
                self.largeRoom = self.bc
            self.largeRoom = self.solver(self.largeRoom,'Dirichlet')
        elif self.room == 'SmallW':
            if self.bc != None:
                self.smallRoomW  = self.bc
            self.smallRoomW = self.solver(self.smallRoomW, 'Neumann','east')
        elif self.room == 'SmallE':
            if self.bc != None:
                self.smallRoomE = self.bc
            self.smallRoomE = self.solver(self.smallRoomE,'Neumann','west')
    
    def smoothing(self,room,roomOld):
        return self.w*room+(1-self.w)*roomOld
        
        
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
        emptySpace= zeros([dim1,dim2])
        emptySpace[:,:] = None
        emptySpace[:,0] = 15
        self.smallRoomE = vstack([self.smallRoomE,emptySpace])
        emptySpace = fliplr(emptySpace)
        self.smallRoomW = vstack([emptySpace,self.smallRoomW])
        plotRoom= hstack([self.smallRoomW,self.largeRoom[:,1:-1],self.smallRoomE])
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
        grid = zeros([X/(dx)+1,Y/(dx)+1])
        grid = self._initbc(grid,size,dir)
        return grid

        
    
    def _initbc(self,grid,size,dir=None):
        gH = 40
        gW = 5
        gN = 15
        if size == 'small':
            grid[0,:] = gN
            grid[-1,:] = gN
            grid[:,-1] = gN
            grid[:,0] = gH
            if dir == 'west':
                return grid
            elif dir == 'east':
                grid = fliplr(grid)
                return grid
        else:
            grid[:,0]=gN
            grid[: ,-1] = gN
            grid[0,:] = gH
            grid[-1,:] = gW
            print grid
            return grid
        
