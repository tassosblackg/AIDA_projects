# HW2 implement Graphplan algorithm for HW1 data
# Planning & Scheduling Class | MSc AIDA,UoM
# Tassos Karageorgiadis aid21002
# github:@tassosblackg


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
    if (t[1]==1):
        for obj in objects.items():
            for place in places.items():
                at_fact = Fact(fact_counter,t[0],[ obj[1], place[1] ])
                fact_space.append(at_fact)
                fact_counter += 1 # increase counter of id
    # 'on'
    elif (t[1]==2):
        for obj in objects.items():
            if ('crate' in obj[0] ):
                for obj2 in objects.items():
                    if( 'pallet' in obj2[0]):
                        on_fact = Fact(fact_counter,t[0],[ obj[1],obj2[1] ])
                        fact_space.append(on_fact)
                        fact_counter += 1 # increase counter of id

print(len(fact_space))
for i in fact_space:
    print(i.id,i.type,i.obj_id)
