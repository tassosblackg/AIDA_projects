# Planning & Scheduling
## HW2 Graphplan
### Tassos Karageorgiadis

## Introduction:
First thing first I passed the problem data into proper data structures like python dictionaries. I split the data into 3 dictionaries one contains all the objects, a second one containing all the locations/places and third one dictionary with fact types.

**objects** = *{ 'truck0':1,'truck1':2,'pallet0':3,'pallet1':4,'pallet2':5,'crate0':6,'crate1':7,'hoist0':8,'hoist1':9,'hoist2':10}*

**places** = *{'depot0':0,'distributor0':1,'distributor1':2}*

**facts_types** = *{'at':1,'on':2,'in':3,'lifting':4,'available':5,'clear':6}*


**Important notice** : all objects are locatable, fact 'on' is only (crate, pallet) or (crate,crate) pairs, fact 'in' (crate,trucks) pairs, fact 'lifting' is only (hoist,crate) pairs, fact 'available' has as object values only hoist and fact 'clear' has values of crates or pallet objects.

## Question A:
For this part of the assignment from all the above data created two list with all possible combinations of facts and actions. So, created a file with all facts (*facts_space.txt*) and one file with all actions (*actions_space.txt*).

For each ground fact inside *fact_space.txt* there is one fact increasing counter as id, one variable showing the type of predicate, and a list containing all the object id/integers from object dictionary.

For each ground action inside *action_space.txt* there is an action id, the action's type, the list with parameters values which are corresponding to an object id/value for the objects dictionary. Then there is a list with all the preconditions, in this list every precondition is an *object of class Predicate* and contains one attribute for the predicate type, and one list with the objects that form the predicate-relation. Afterward, there are two more lists one for all the positive effects of an action, and then a negative effects list showing a 'not' logic relation for a specific predicate. Every single effect either positive or negative is a *Predicate class* object. Not forget to mention that for all the preconditions, positive or negative effects inside these lists there is a logic 'and' relation between list's object.

With all these being said, the next step was to iterate through multiple for-loops in order to get all the possible combinations of facts or actions given some assumption like *trucks deliver only crates not pallets* or *pallets can't be in the top of a crate*. Those assumptions helped to reduce the total fact and actions space containing only the option that make sense to us.

## Question B:
In this part I had to implement a Graphplan algorithm approach. So, the basic idea behind this was to represent the graphplan schema as a linked-list, where each *State(Si) or Action(Ai) level* of the graph is a list containing objects of type *FactNode* for states, and *ActionNode* for actions, where for each type of node keeps a left-wing sibling of type list which contains the connections to the left level by using the id of each fact/action of state/actions level and then there is a right-wing sibling of type list. Then I had to find the mutex relations for each level(actions or states) of the linked-list/graph. The concept behind the mutex relations is to compare list of objects e.g. preconditions list of an action with the previous level's states facts, in order to define if a action can occur,etc. So, at the end the Graphplan problem becomes a search problem and more specific a  Constraints Satisfaction Problem (if we see mutexes as constraints). In each step we expand the graph by Actions and new States (outcome of effects) while checking the mutexes to verify them. If two continuous States have exactly the same facts inside then the algorithm stops and doesn't expand any more. And at the end tries to find backwards-search for a solution if there is any --that means that in the last state we have our goals as facts.

**Unluckily I haven't manage to implement the Graphplan algorithm on time, the design, and the requirements specification took me more time than I expected**.
