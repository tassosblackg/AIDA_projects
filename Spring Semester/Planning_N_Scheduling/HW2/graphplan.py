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
