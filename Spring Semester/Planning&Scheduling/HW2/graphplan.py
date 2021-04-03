# HW2 implement Graphplan algorithm for HW1 data
# Planning & Scheduling Class | MSc AIDA,UoM
# Tassos Karageorgiadis aid21002
# github:@tassosblackg

import os

class StateNode():

    def __init__(self):
        self.name = ""
        self.leftSibling = []
        self.rightSibling = []

class ActionNode():
    def __init__(self):
        self.name = ""
        self.leftSibling = []
        self.rightSibling = []

class Action():

    def __init__(self):
        self.name = ""
        self.precond = []
        self.effects = []
