# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:39:45 2017

@author: Vandan
"""

#OBJECTIVE 1: minimize production and transportation cost from warehouse to customers

from gurobipy import *
import math
import pdb

m = Model()

#import data

import csv

#reading distance data csv into a dictionary: dist[(i,j)]
readDist = csv.reader(open('DistPlantWarehouse.csv'))
next(readDist) #skips the headers
dist = {}
for row in readDist:
	key1=int(row[0])
	key2=int(row[1])
	dist[(key1,key2)]=float(row[2])
	
#reading demand data csv into a dictionary: dem[(j,k)]
readDem = csv.reader(open('DemandWarehouseProduct.csv'))
next(readDem) #skips the headers
dem = {}
for row in readDem:
	key1=int(row[0])
	key2=int(row[1])
	dem[(key1,key2)]=float(row[2])

#reading plant production constraint: p[(i,k)]
readp = csv.reader(open('PlantProductConstraints.csv'))
next(readp) #skips the headers
p = {}
for row in readp:
	key1=int(row[0])
	key2=int(row[1])
	p[(key1,key2)]=float(row[2])
	
#reading production capacity-product: cap[(i,k)]
readcap = csv.reader(open('ProdCapPlantProduct.csv'))
next(readcap) #skips the headers
cap = {}
for row in readcap:
	key1=int(row[0])
	key2=int(row[1])
	cap[(key1,key2)]=float(row[2])
	
#reading regular and overtime cost: reg[k], ovr[k]
readcost = csv.reader(open('CostProductRegOvertime.csv'))
next(readcost) #skips the headers
reg = {}
ovr = {}
for row in readcost:
	key1=int(row[0])
	reg[key1]=float(row[1])
	ovr[key1]=float(row[2])
	
#initialize parameters
x={}
y={}
t=0.12 #FTL= 60% of LTL
reghours= 2880 #hours/year (=12months*30days*8hours)
ovrhours= 1440 #hours/year (=12months*30days*4hours)

#number of plants: i = 4
#number of warehouses: j = 5
#number of products: k = 5

pdb.set_trace()

#Adding decision variables:
	
#xijk=> Qty (tonns) mfg at regular time and shipped from plant 'i' to warehouse 'j' of type 'k'
for i in range(1,5):
	for j in range(1,6):
		for k in range(1,6):
			x[(i,j,k)] = m.addVar(lb = 0, vtype = GRB.CONTINUOUS, name ="x%d,%d,%d" % (i,j,k))
	
#yijk=> Qty (tonns) mfg at over time and shipped from plant 'i' to warehouse 'j' of type 'k'
for i in range(1,5):
	for j in range(1,6):
		for k in range(1,6):
			y[(i,j,k)] = m.addVar(lb = 0, vtype = GRB.CONTINUOUS, name ="y%d,%d,%d" % (i,j,k))
			
m.update()

pdb.set_trace()

#Adding constraints

#demand satisfaction constraint
for j in range(1,6):
		for k in range(1,6):
			m.addConstr(quicksum((x[(i,j,k)] + y[(i,j,k)]) for i in range(1,5)) == dem[(j,k)])

pdb.set_trace()
			
#production capacity
for i in range(1,5):
		for k in range(1,6):
			m.addConstr(quicksum((x[(i,j,k)] + y[(i,j,k)]) for j in range(1,6)) <= p[(i,k)]*cap[(i,k)])

pdb.set_trace()

#production constraints on regular and overtime production

#plant1: i=1
#production rate: 100 tonnes/hour
#product1: k=1
#regular
m.addConstr(quicksum(x[(1,j,1)] for j in range(1,6)) <= reghours*100)
#over time
m.addConstr(quicksum(y[(1,j,1)] for j in range(1,6)) <= ovrhours*100)

pdb.set_trace()

#plant2: i=2
#production rate: 50 tonnes/hour
#product2: k=2
#regular
m.addConstr(quicksum(x[(2,j,2)] for j in range(1,6)) <= reghours*50)
#over time
m.addConstr(quicksum(y[(2,j,2)] for j in range(1,6)) <= ovrhours*50)

#plant3: i=3
#production rate: 50 tonnes/hour
#product3: k=3
#regular
m.addConstr(quicksum(x[(3,j,3)] for j in range(1,6)) <= reghours*50)
#over time
m.addConstr(quicksum(y[(3,j,3)] for j in range(1,6)) <= ovrhours*50)
						
#plant4: i=4
#production rate: 50 tonnes/hour
#product4: k=4
#regular
m.addConstr(quicksum(x[(4,j,4)] for j in range(1,6)) <= reghours*50)
#over time
m.addConstr(quicksum(y[(4,j,4)] for j in range(1,6)) <= ovrhours*50)			

#plant4: i=4
#production rate: 50 tonnes/hour
#product5: k=5
#regular
m.addConstr(quicksum(x[(4,j,5)] for j in range(1,6)) <= reghours*50)
#over time
m.addConstr(quicksum(y[(4,j,5)] for j in range(1,6)) <= ovrhours*50)				
			

pdb.set_trace()

#Setting objective function
#obj= production cost+ transportation cost
m.setObjective(quicksum((reg[k]*x[(i,j,k)]+ovr[k]*y[(i,j,k)]) for i in range(1,5) for j in range(1,6) for k in range(1,6)) + quicksum(((x[(i,j,k)]+y[(i,j,k)])*t*dist[(i,j)]) for i in range(1,5) for j in range(1,6) for k in range(1,6)))

pdb.set_trace()

m.optimize()			
			
# getting gurobi output into normal dictionaries
x_flow={}
for i in range(1,5):
	for j in range(1,6):
		for k in range(1,6):
			x_flow[(i,j,k)]=x[(i,j,k)].x			

y_flow={}
for i in range(1,5):
	for j in range(1,6):
		for k in range(1,6):
			y_flow[(i,j,k)]=y[(i,j,k)].x	
			
			
			
#to write the output in an excel
import pandas as pd
pd.DataFrame(x_flow, index=[0]).to_csv('x_flow.csv')
pd.DataFrame(y_flow, index=[0]).to_csv('y_flow.csv')