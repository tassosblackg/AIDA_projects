# HW2 implement Graphplan algorithm for HW1 data
# Planning & Scheduling Class | MSc AIDA,UoM
# Tassos Karageorgiadis aid21002
# github:@tassosblackg

import sys

class Fact():

    def __init__(self,counter,type,objectsL):
        self.id = counter
        self.type = type
        self.obj_id = objectsL


class Action():

    def __init__(self,counter):
        self.id = counter
        self.params = []
        self.precond = []
        self.pos_eff = []
        self.neg_eff = []


# Graphplan Algo Components are part of a Linked-List
class ActionNode(Action):
    def __init__(self):
        self.leftSibling = []
        self.rightSibling = []

class FactNode(Fact):
    def __init__(self):
        self.leftSibling = []
        self.rightSibling = []



'''
Input Data passed trough by hand
'''

# all objects which are locatable of the problem
objects = { 'truck0':1,'truck1':2,'pallet0':3,'pallet1':4,'pallet2':5,'crate0':6,'crate1':7,
            'hoist0':8,'hoist1':9,'hoist2':10}

# Locations Data
places = {'depot0':0,'distributor0':1,'distributor1':2}

facts_types = {'at':1,'on':2,'in':3,'lifting':4,'available':5,'clear':6}

fact_space,action_space = [],[]

# 'at' combinations
fact_counter = 1
for t in facts_types.items():
    # 'at'
    if ( t[1] == 1 ):
        for obj in objects.items():
            for place in places.items():
                at_fact = Fact(fact_counter,t[0],[ obj[1], place[1] ])
                fact_space.append(at_fact)
                fact_counter += 1 # increase counter of id
    # 'on'
    elif ( t[1] == 2 ):
        for obj in objects.items():
            if ('crate' in obj[0] ):
                for obj2 in objects.items():
                    if( 'pallet' in obj2[0]):
                        on_fact = Fact(fact_counter,t[0],[ obj[1],obj2[1] ])
                        fact_space.append(on_fact)
                        fact_counter += 1 # increase counter of id
    # 'in'
    elif ( t[1] == 3 ):
            for obj in objects.items():
                if ('crate' in obj[0] ):
                    for obj2 in objects.items():
                        if( 'truck' in obj2[0]):
                            in_fact = Fact(fact_counter,t[0],[ obj[1],obj2[1] ])
                            fact_space.append(in_fact)
                            fact_counter += 1 # increase counter of id
    # 'lifting'
    elif ( t[1] == 4 ):
        for obj in objects.items():
            if ('hoist' in obj[0] ):
                for obj2 in objects.items():
                    if( 'crate' in obj2[0]):
                        lifting_fact = Fact(fact_counter,t[0],[ obj[1],obj2[1] ])
                        fact_space.append(lifting_fact)
                        fact_counter += 1 # increase counter of id
    # 'available'
    elif ( t[1] == 5 ):
        for obj in objects.items():
            if ('hoist' in obj[0] ):
                        av_fact = Fact(fact_counter,t[0],[ obj[1] ])
                        fact_space.append(av_fact)
                        fact_counter += 1 # increase counter of id
    # 'clear'
    elif ( t[1] == 6 ):
        for obj in objects.items():
            if ( ('crate' in obj[0]) or ('pallet' in obj[0]) ):
                        clear_fact = Fact(fact_counter,t[0],[ obj[1] ])
                        fact_space.append(clear_fact)
                        fact_counter += 1 # increase counter of id
    else:
        print('\nError case in facts space building...\n')

# Testing -- Facts Space -Q:a
print('\n*Total facts spce size = ',len(fact_space))

original_stdout = sys.stdout # save a ref to init stdout
with open('facts_space.txt','w') as f:
    sys.stdout = f
    for i in fact_space:
        print('Fact_id = ',i.id,i.type,' objects_IDs= ',i.obj_id)
    sys.stdout = original_stdout # reset stdout
