# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 17:17:24 2015

@author: Edward
"""
import sys
from mpi4py import MPI
import numpy
import RoomHeating
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n = int(sys.argv[1])
bcW = numpy.zeros(1)
bcE = numpy.zeros(1)
bc2 = numpy.zeros(1)
room = RoomHeating.roomHeating(1/20.)


for i in range(n):

    if rank == 2: ## Small Room East
        #comm.Recv(bc2,source=0)
        bcW[0] = 10
        comm.Send(bcW,dest=0)
        print bc2[0]


    if rank == 1: ## Small Room West
        bcE[0] = 2
        comm.Send(bcE,dest=0)



    if rank == 0: ##Large Room
        if i==0:
            Large = room(1,1,'Large')
        comm.Recv(bcW,source=1)
        comm.Recv(bcE,source=2)
        print bcE, bcW
        bc2[0]  =5
        #comm.Send(bc2,dest=1)