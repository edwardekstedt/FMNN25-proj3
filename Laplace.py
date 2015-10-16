# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:34:39 2015

@author: Edward
"""

from numpy import *
from mpi4py import MPI
from scipy import *


class laplaceSolver(object):
    
    def __init__(self,bc,dx):
        self.bc = bc
        self.dx = dx
        [self.N, self.M] = bc.shape
        #N = AMOUNT OF ROWS
        #M = AMOUNT OF COLUMNS
        self.N = self.N-2
        self.M = self.M-2
        
    def __call__(self,condition):
        self._setRhs(condition)
        return self._update()

    def _setRhs(self,condition):
        if condition == 'Dirichlet':
            self.rhs = zeros([self.N,self.M])
            self.rhs[0,:] =- self.bc[0,1:-1]
            self.rhs[-1,:] =- self.bc[-1,1:-1]
            self.rhs[:,0] = self.rhs[:,0]- self.bc[1:-1,0]
            self.rhs[:,-1] = self.rhs[:,-1] - self.bc[1:-1,-1]
            self.rhs = self.rhs/self.dx**2
        if condition == 'Neumann':
            self.rhs
    def _update(self):
        self.rhs = self.rhs.reshape(self.M*self.N)
        sub = ones([1,self.M-1])
        main = (-4*ones([1,self.M]))
        D = diagflat(main) + diagflat(sub,1) + diagflat(sub,-1)
        BL = kron(eye(self.N),D)
        T = BL+diagflat(ones([1,self.M*(self.N-1)]),-self.M)+diagflat(ones([1,self.M*(self.N-1)]),self.M)
        T = T*1/self.dx**2      
        U = linalg.solve(T,self.rhs)
        U = U.reshape(self.N,self.M)
        self.bc[1:-1,1:-1] = U
        return self.bc
 
M = array([[40.,40,40,40],[15,0,0,15],[15,0,0,15],[15,0,0,15],[15,0,0,15],[15,0,0,15],[5,5,5,5]])
solved = laplaceSolver(M,1/3.)
U = solved('Dirichlet')
print(U)