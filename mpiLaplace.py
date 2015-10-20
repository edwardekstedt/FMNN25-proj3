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
dx = float(sys.argv[2])
bcW = numpy.zeros([int(1/dx-1),1])
bcE = numpy.zeros([int(1/dx-1),1])
neumannW = numpy.zeros([int(1/dx-1),1])
neumannE = numpy.zeros([int(1/dx-1),1])
room = RoomHeating.roomHeating(dx)
N = 2/(dx)+1
SmallE = numpy.zeros([N/2+1,N/2+1])
SmallW = numpy.zeros([N/2+1,N/2+1])
for i in range(n):

    if rank == 2: ## Small Room East
        comm.Recv(neumannE,source=0)
        #print 'Eastern Neumann recieved'
        SmallE = room.smallRoomE
        SmallE[1:-1,0] = neumannE.T
        SmallE = room('SmallE',SmallE)
        bcE = SmallE[1:-1,0]
        if i==n-1:
            comm.Send(numpy.ascontiguousarray(SmallE),dest=0)
        else:
            comm.Send(numpy.ascontiguousarray(bcE),dest=0)


    if rank == 1: ## Small Room West
        comm.Recv(neumannW,source=0)
        #print 'Western Neumann recieved'
        SmallW = room.smallRoomW
        SmallW[1:-1,-1]= neumannW.T
        SmallW = room('SmallW',SmallW)
        bcW = SmallW[1:-1,-1]
        if i ==n-1:
            comm.Send(numpy.ascontiguousarray(SmallW),dest=0)
        else:
            comm.Send(numpy.ascontiguousarray(bcW),dest=0)


    if rank == 0: ##Large Room
        if i==0:
            Large = room('Large')
        else:
            comm.Recv(bcW,source =1)
           # print 'bcW recieved in iteration',i+1
            comm.Recv(bcE,source =2)
          #  print 'bcE recieved in iteration',i+1
            Large[N/2+1:-1,0] = bcW.T
            Large[1:N/2,-1] = bcE.T
            Large = room('Large',Large)
        neumannW = -(Large[N/2+1:-1,0]-Large[N/2+1:-1,1])/dx
        neumannE = -(Large[1:N/2,-1]-Large[1:N/2,-2])/dx
        comm.Send(neumannW,dest=1)
        comm.Send(neumannE,dest=2)
        if i==n-1:
            comm.Recv(SmallE,source=2)
            comm.Recv(SmallW,source=1)
            room.smallRoomE= SmallE
            room.smallRoomW = SmallW
            room.plot()
        
    