# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:55:54 2015

@author: Edward
"""
from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()

a = 6.0
b = 3.0

if rank == 0:
    print(a+b)
if rank == 1:
    print(a*b)
if rank == 2:
    print(max(a,b))