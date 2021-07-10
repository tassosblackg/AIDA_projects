# HW2 implement Graphplan algorithm for HW1 data
# Planning & Scheduling Class | MSc AIDA,UoM
# Tassos Karageorgiadis aid21002
# github:@tassosblackg

import sys


class Fact:
    def __init__(self, counter, type, objectsL):
        self.id = counter
        self.type = type
        self.obj_id = objectsL


class Action:
    def __init__(self, counter, n, param):
        self.id = counter
        self.name = n
        self.params = param
        self.precond = []
        self.pos_eff = []  # actual effect
        self.neg_eff = []  # effect with a not logic

    # add Preconditions
    def addPrec(self, precond_l):
        self.precond.append(Predicate(precond_l))

    # add Positive effects
    def addPos_eff(self, pos_l):
        self.pos_eff.append(Predicate(pos_l))

    # add Negative effects
    def addNeg_eff(self, neg_l):
        self.neg_eff.append(Predicate(neg_l))


class Predicate:
    def __init__(self, objl):
        self.type = objl[0]
        self.objects = objl[1:]


# Graphplan Algo Components are part of a Linked-List
class ActionNode(Action):
    def __init__(self):
        self.leftSibling = []
        self.rightSibling = []


class FactNode(Fact):
    def __init__(self):
        self.leftSibling = []
        self.rightSibling = []


"""
Input Data passed trough by hand
"""

# all objects which are locatable of the problem
objects = {
    "truck0": 1,
    "truck1": 2,
    "pallet0": 3,
    "pallet1": 4,
    "pallet2": 5,
    "crate0": 6,
    "crate1": 7,
    "hoist0": 8,
    "hoist1": 9,
    "hoist2": 10,
}

# Locations Data
places = {"depot0": 0, "distributor0": 1, "distributor1": 2}

facts_types = {"at": 1, "on": 2, "in": 3, "lifting": 4, "available": 5, "clear": 6}

fact_space, action_space = [], []

"""
    Create Facts Space aka all possible facts
"""
# 'at' combinations
fact_counter = 1
for t in facts_types.items():
    # 'at'
    if t[1] == 1:
        for obj in objects.items():
            for place in places.items():
                at_fact = Fact(fact_counter, t[0], [obj[1], place[1]])
                fact_space.append(at_fact)
                fact_counter += 1  # increase counter of id
    # 'on'
    elif t[1] == 2:
        for obj in objects.items():
            if "crate" in obj[0]:
                for obj2 in objects.items():
                    if ("pallet" in obj2[0]) or ("crate" in obj2[0]):
                        on_fact = Fact(fact_counter, t[0], [obj[1], obj2[1]])
                        fact_space.append(on_fact)
                        fact_counter += 1  # increase counter of id
    # 'in'
    elif t[1] == 3:
        for obj in objects.items():
            if "crate" in obj[0]:
                for obj2 in objects.items():
                    if "truck" in obj2[0]:
                        in_fact = Fact(fact_counter, t[0], [obj[1], obj2[1]])
                        fact_space.append(in_fact)
                        fact_counter += 1  # increase counter of id
    # 'lifting'
    elif t[1] == 4:
        for obj in objects.items():
            if "hoist" in obj[0]:
                for obj2 in objects.items():
                    if "crate" in obj2[0]:
                        lifting_fact = Fact(fact_counter, t[0], [obj[1], obj2[1]])
                        fact_space.append(lifting_fact)
                        fact_counter += 1  # increase counter of id
    # 'available'
    elif t[1] == 5:
        for obj in objects.items():
            if "hoist" in obj[0]:
                av_fact = Fact(fact_counter, t[0], [obj[1]])
                fact_space.append(av_fact)
                fact_counter += 1  # increase counter of id
    # 'clear'
    elif t[1] == 6:
        for obj in objects.items():
            if ("crate" in obj[0]) or ("pallet" in obj[0]):
                clear_fact = Fact(fact_counter, t[0], [obj[1]])
                fact_space.append(clear_fact)
                fact_counter += 1  # increase counter of id
    else:
        print("\nError case in facts space building...\n")

# Testing -- Facts Space -Q:a


original_stdout = sys.stdout  # save a ref to init stdout
with open("facts_space.txt", "w") as f:
    sys.stdout = f
    print("\n*Total facts space size = ", len(fact_space))
    for i in fact_space:
        print("Fact_id = ", i.id, i.type, " objects_IDs= ", i.obj_id)
    sys.stdout = original_stdout  # reset stdout


"""
Action Space all possible actions

"""
action_types = {"Drive": 1, "Lift": 2, "Drop": 3, "Load": 4, "Unload": 5}
crates = {"crate0", "crate1"}
pallets = {"pallet0", "pallet1", "pallet2"}
trucks = {"truck0", "truck1"}

crates_dictionary = dict(map(lambda key: (key, objects.get(key, None)), crates))
pallets_dictionary = dict(map(lambda key: (key, objects.get(key, None)), pallets))
trucks_dictionary = dict(map(lambda key: (key, objects.get(key, None)), trucks))
# print(crates_dictionary)
# print(pallets_dictionary)
action_counter = 0

for obj in objects.items():
    if "truck" in obj[0]:
        for source in places.items():  # get source place
            for destination in places.items():  # get destination place
                if destination[1] != source[1]:
                    # new action
                    d_action = Action(
                        action_counter,
                        "Drive",
                        [obj[1], source[1], destination[1]],
                    )
                    # add precondition for action
                    d_action.addPrec(["at", obj[1], source[1]])
                    # add positive effect
                    d_action.addPos_eff(["at", obj[1], destination[1]])
                    # add negative precond not('predicate',?x,?y)
                    d_action.addNeg_eff(["at", obj[1], source[1]])

                    action_space.append(d_action)
                    action_counter += 1

    elif "hoist" in obj[0]:  # all actions starts with hoist as first args
        # Lift n Drop actions
        for crate in crates_dictionary.items():
            # Lift Drop Actions combinations
            for surf in pallets_dictionary.items():
                for place in places.items():
                    li_action = Action(
                        action_counter, "Lift", [obj[1], crate[1], surf[1], place[1]]
                    )
                    li_action.addPrec(["at", obj[1], place[1]])
                    li_action.addPrec(["available", obj[1]])
                    li_action.addPrec(["at", crate[1], place[1]])
                    li_action.addPrec(["on", crate[1], surf[1]])
                    li_action.addPrec(["clear", crate[1], surf[1]])

                    # add positive effect
                    li_action.addPos_eff(["lifting", obj[1], crate[1]])
                    li_action.addPos_eff(["clear", surf[1]])

                    # add negative precond not('predicate',?x,?y)
                    li_action.addNeg_eff(["at", crate[1], place[1]])
                    li_action.addNeg_eff(["clear", surf[1]])
                    li_action.addNeg_eff(["available", obj[1]])
                    li_action.addNeg_eff(["on", crate[1], surf[1]])

                    action_space.append(li_action)
                    action_counter += 1

                    # Drop
                    drop_action = Action(
                        action_counter, "Drop", [obj[1], crate[1], surf[1], place[1]]
                    )
                    drop_action.addPrec(["at", obj[1], place[1]])
                    drop_action.addPrec(["at", surf[1], place[1]])
                    drop_action.addPrec(["clear", surf[1]])
                    drop_action.addPrec(["lifting", obj[1], crate[1]])

                    drop_action.addPos_eff(["available", obj[1]])
                    drop_action.addPos_eff(["at", crate[1], surf[1]])
                    drop_action.addPos_eff(["clear", crate[1]])
                    drop_action.addPos_eff(["on", crate[1], surf[1]])

                    drop_action.addNeg_eff(["lifting", obj[1], crate[1]])
                    drop_action.addNeg_eff(["clear", surf[1]])

                    action_space.append(drop_action)
                    action_counter += 1

            # Load Unload Actions
            for tr in trucks_dictionary.items():
                for place in places.items():
                    # Load
                    lo_action = Action(
                        action_counter, "Load", [obj[1], crate[1], tr[1], place[1]]
                    )
                    lo_action.addPrec(["at", obj[1], place[1]])
                    lo_action.addPrec(["at", tr[1], place[1]])
                    lo_action.addPrec(["lifting", obj[1], crate[1]])

                    lo_action.addPos_eff(["in", crate[1], tr[1]])
                    lo_action.addPos_eff(["available", obj[1]])

                    lo_action.addNeg_eff(["lifting", obj[1], crate[1]])

                    action_counter += 1
                    action_space.append(lo_action)

                    # Unload
                    unlo_action = Action(
                        action_counter, "UnLoad", [obj[1], crate[1], tr[1], place[1]]
                    )
                    unlo_action.addPrec(["at", obj[1], place[1]])
                    unlo_action.addPrec(["at", tr[1], place[1]])
                    unlo_action.addPrec(["available", obj[1]])
                    unlo_action.addPrec(["in", crate[1], tr[1]])

                    unlo_action.addPos_eff(["lifting", obj[1], crate[1]])

                    unlo_action.addNeg_eff(["in", crate[1], tr[1]])
                    unlo_action.addNeg_eff(["available", obj[1]])

                    action_counter += 1
                    action_space.append(unlo_action)

# print(len(action_space))
# for j in action_space:
#     print(j.id, j.name)

original_stdout = sys.stdout  # save a ref to init stdout
with open("actions_space.txt", "w") as f:
    sys.stdout = f
    print("\n*Total actions space size = ", len(action_space))
    for j in action_space:
        print("\nAction_id = ", j.id, j.name, " params= ", j.params)
        print("*preconditions:")
        for prec in j.precond:
            print(" ", prec.type, prec.objects)
        print("*positive effects:")
        for pos_e in j.pos_eff:
            print(" ", pos_e.type, pos_e.objects)
        print("*negative (not) effects:")
        for neg_e in j.neg_eff:
            print(" ", neg_e.type, neg_e.objects)
        print("------------------------------------------------------------")
    sys.stdout = original_stdout  # reset stdout
