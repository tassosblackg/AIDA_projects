# Planning & Scheduling
## HW2 Graphplan
### Tassos Karageorgiadis

## Introduction:
First thing first I passed the problem data into proper data structures like python dictionaries. I split the data into 3 dictionaries one contains all the objects, a second one containing all the locations/places and third one dictionary with fact types.

**objects** = *{ 'truck0':1,'truck1':2,'pallet0':3,'pallet1':4,'pallet2':5,'crate0':6,'crate1':7,'hoist0':8,'hoist1':9,'hoist2':10}*

**places** = *{'depot0':0,'distributor0':1,'distributor1':2}*

**facts_types** = *{'at':1,'on':2,'in':3,'lifting':4,'available':5,'clear':6}*


**Important notice** : all objects are locatable, fact 'on' is only crate, pallet pairs, fact 'in' crate,trucks pairs, fact 'lifting' is only hoist,crate pairs, fact 'available' has as object values only hoist and fact 'clear' has values of crates or pallet objects.

## Question A:
For this part of the assignment from all the above data created two list with all possible combinations of facts and actions. So, created a file with all facts (*facts_space.txt*) and one file with all actions (*actions_space.txt*). 
