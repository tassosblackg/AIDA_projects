# import matplotlib
# import matplotlib.pyplot as plt
# sorting explanation https://www.geeksforgeeks.org/sorted-function-python/

def powerset(items):
	res = [[]]
	for item in items:
		newset = [r+[item] for r in res]
		res.extend(newset)
	return res

def knapsack_brute_force(items, max_weight):
	knapsack = []
	best_weight = 0
	best_value = 0
	for item_set in powerset(items):
		set_weight = sum(map(weight, item_set))
		set_value = sum(map(value, item_set))
		if set_value > best_value and set_weight <= max_weight:
			best_weight = set_weight
			best_value = set_value
			knapsack = item_set
	return knapsack, best_weight, best_value

def weight(item):
    # print('\n|W|',item)
    return item[1]

def value(item):
	return item[2]

def density(item):
	return float(value(item))/weight(item)

# items: [(id, weight, value)]
def knapsack_greedy(items, max_weight, keyF=weight):
    knapsack = []
    knapsack_weight = 0
    knapsack_value = 0
    # print('\n$$$ ',keyF)
    items_sorted = sorted(items, key=keyF)
    # print('\n# ->',items_sorted)
    while len(items_sorted) > 0:
    	item = items_sorted.pop()
    	if weight(item) + knapsack_weight <= max_weight:
    		knapsack.append(item)
    		knapsack_weight += weight(knapsack[-1])
    		knapsack_value += value(knapsack[-1])
    	else:
    		break
    return knapsack, knapsack_weight, knapsack_value

def build_items(n):
	from random import random
	res = []
	for i in range(n):
		res.append((i, 1+int(9*random()), 1+int(9*random())))
	return res

#items = [(0,2,4), (1,5,3), (2,7,4), (3,3,5)]
res = []
sims = 1

for i in range(sims):
    items = build_items(10)
    max_weight = 20
    print(items,type(items))
    weight(items)
    print('wwwwwwwww')
    # knapsack, opt_wt, opt_val = knapsack_brute_force(items, max_weight)
    # print("\n@  ",knapsack, opt_wt, opt_val)
    r = []
    # #print 'weight'
    # knapsack, wt, val = knapsack_greedy(items, max_weight, weight)
    # r.append(float(val)/opt_val)
    #print 'value'
    knapsack, wt, val = knapsack_greedy(items, max_weight, value)
    print(knapsack,wt, val)
    r.append(float(val)/opt_val)
    #print 'density'
    knapsack, wt, val = knapsack_greedy(items, max_weight, density)
    r.append(float(val)/opt_val)
    res.append(r)

print( [e[0] for e in res])

# plt.scatter(range(sims), [e[0] for e in res], c='r', marker='s', s=20)
# #plt.scatter(range(sims), [e[1] for e in res], c='b', marker='x', s=20)
# plt.show()
