# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 00:14:12 2017

@author: Vandan
"""
#OBJECTIVE 1: minimize number of warehouses and transportation cost from warehouse to customers

from gurobipy import *
import math
import pdb


m = Model()

#import data

import csv

#reading distance data csv into a dictionary
readDist = csv.reader(open('DistancesWithinSites.csv'))
next(readDist) #skips the headers
dist = {}
for row in readDist:
	key1=int(row[0])
	key2=int(row[1])
	dist[(key1,key2)]=float(row[2])

#reading demand data csv into a dictionary
readDem = csv.reader(open('DemandCustomerProduct.csv'))
next(readDem) #skips the headers
dem = {}
for row in readDem:
	key1=int(row[0])
	key2=int(row[1])
	dem[(key1,key2)]=float(row[2])


#initialize parameters
x={}
y={}
R={}
o=10000000 #fixed opening cost ($)
t=0.2 #transportation cost LTL ($/ton/mile)
u=100000 #capacity of the warehouse (tonnes)
#setup the Range dictionary 
for i in range(1,51):
	for j in range(1,51):
		if dist[(i,j)]<=500.0:
			R[(i,j)]=1
		else:
			R[(i,j)]=0
       

#Adding decision variables

#yes/no variable, yi=>1 if warehouse to be open at 1
for i in range(1,51):
	y[i] = m.addVar(vtype = GRB.BINARY, name = "y%d" % i)

	
#if yes then how what is the flow?
#xijk=> Qty (tonns) shipped from 'i' to 'j' of type 'k'
for i in range(1,51):
	for j in range(1,51):
		for k in range(1,6):
			x[(i,j,k)] = m.addVar(lb = 0, vtype = GRB.CONTINUOUS, name ="x%d,%d,%d" % (i,j,k))


m.update()


#Adding constraints

#demand satisfcation constraint
for j in range(1,51):
		for k in range(1,6):
			m.addConstr(quicksum(x[(i,j,k)] for i in range(1,51)) == dem[(j,k)])


#potential capacity constraint and supply only if warehouse open constraint
for i in range(1,51):
	m.addConstr(quicksum(x[(i,j,k)] for j in range(1,51) for k in range(1,6)) <= u*y[i] )
	

#Coverage 80% demand within 500 miles constraint, (supply from i >= 0.8 total supply from i)
for i in range(1,51):
	m.addConstr(quicksum(R[(i,j)]*x[(i,j,k)] for j in range(1,51) for k in range(1,6)) >= 0.8*(quicksum(R[(i,j)]*x[(i,j,k)] for j in range(1,51) for k in range(1,6))))


#Setting objective function
m.setObjective( o*quicksum(y[i] for i in range(1,51)) + quicksum(t*dist[(i,j)]*x[(i,j,k)] for i in range(1,51) for j in range(1,51) for k in range(1,6)))


m.optimize()

#for v in m.getVars():
#		print(v.varName, v.x)

# getting gurobi output into normal dictionaries
x1_flow={}
for i in range(1,51):
	for j in range(1,51):
		for k in range(1,6):
			x1_flow[(i,j,k)]=x[(i,j,k)].x

y1_loc={}
for i in range(1,51):
	y1_loc[i]=y[i].x
			
# total units from i to all j of type k
#sum(x_flow[(i,j,k)] for i in [5] for j in range(1,51) for k in [2])

#to export the output into csv
#import pandas as pd
#pd.DataFrame(x1_flow, index=[0]).to_csv('x1_flow.csv')
#pd.DataFrame(y1_loc, index=[0]).to_csv('y1_flow.csv')





			


