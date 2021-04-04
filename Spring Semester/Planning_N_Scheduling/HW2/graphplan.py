# HW2 implement Graphplan algorithm for HW1 data
# Planning & Scheduling Class | MSc AIDA,UoM
# Tassos Karageorgiadis aid21002
# github:@tassosblackg


class FactNode():

    def __init__(self,counter,type,objectsL):
        self.id = counter
        self.type = type
        self.obj_id = objectsL
        self.leftSibling = []
        self.rightSibling = []

class ActionNode():
    def __init__(self):
        self.name = ""

        self.leftSibling = []
        self.rightSibling = []

class Action():

    def __init__(self,name):
        self.name = name
        self.precond = []
        self.effects = []
