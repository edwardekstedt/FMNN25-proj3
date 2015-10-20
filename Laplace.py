# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:34:39 2015

@author: Edward
"""

from numpy import *


class laplaceSolver(object):
    
    def __init__(self,dx):
        self.dx = dx

        
    def __call__(self,bc,conditionType,dir=None):
        self.bc = bc
        [self.N, self.M] = bc.shape
        #N = AMOUNT OF ROWS
        #M = AMOUNT OF COLUMNS
        self.N = self.N-2
        if conditionType == 'Dirichlet':
            self.M = self.M-2
        elif conditionType == 'Neumann':
            self.M = self.M-1
        else:
            raise NameError('Condition must be either "Dirichlet" or "Neumann".')
        self._setRhs(conditionType,dir)
        return self._update(conditionType,dir)

    def _setRhs(self,conditionType,direction):
        self.rhs = zeros([self.N, self.M])    
        if conditionType == 'Dirichlet':
            self.rhs[0,:] =- self.bc[0,1:-1]
            self.rhs[-1,:] =- self.bc[-1,1:-1]
            self.rhs[:,0] = self.rhs[:,0]- self.bc[1:-1,0]
            self.rhs[:,-1] = self.rhs[:,-1] - self.bc[1:-1,-1]
            self.rhs = self.rhs/self.dx**2
        elif conditionType == 'Neumann':
            if direction == 'east':
                pass
            elif direction =='north':
                self.bc = rot90(self.bc,1)
            elif direction =='west':
                self.bc = rot90(self.bc,2)
            elif direction =='south':
                self.bc = rot90(self.bc,3)
            self.rhs[0,:] = -self.bc[0,1:]/self.dx**2
            self.rhs[-1,:] = -self.bc[-1,1:]/self.dx**2
            self.rhs[:,0] = self.rhs[:,0]- self.bc[1:-1,0]/self.dx**2
            self.rhs[:,-1] = self.rhs[:,-1] - self.bc[1:-1,-1]/self.dx
       
    
    def _update(self,conditionType,direction):
        self.rhs = self.rhs.reshape(self.M*self.N)
        sub = ones([1,self.M-1])           
        if conditionType == 'Dirichlet':
            main = (-4*ones([1,self.M]))
        elif conditionType == 'Neumann':
            main = append([-4*ones([1,self.M-1])],[-3])
        T = diagflat(main) + diagflat(sub,1) + diagflat(sub,-1)
        A = (kron(eye(self.N),T)+diagflat(ones([1,self.M*(self.N-1)]),-self.M)+diagflat(ones([1,self.M*(self.N-1)]),self.M))/self.dx**2
        U = linalg.solve(A,self.rhs)
        U = U.reshape(self.N,self.M)
        if conditionType == 'Dirichlet':
            self.bc[1:-1,1:-1] = U
        elif conditionType == 'Neumann':
            self.bc[1:-1,1:] = U
            if direction == 'east':
                pass
            elif direction =='north':
                self.bc=rot90(self.bc,3)
            elif direction =='west':
                self.bc = rot90(self.bc,2)
            elif direction =='south':
                self.bc = rot90(self.bc,1)
        return self.bc