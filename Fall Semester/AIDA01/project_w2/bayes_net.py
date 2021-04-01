import pandas as pd

df = pd.read_json("input.json")
tree_nodes = df.columns[df.columns!='ProblemName']
print(tree_nodes)

# Parse node data
# for i in tree_nodes:
#     print(df[i].Parents)
#     print(df[i].CPT)


prob2calc = {"B":'T'} # {"A":'True','B':'False'}

# #list(df.B.CPT.keys())[0].split(',') #-> get Parents values,for an evident
def calculate_probs(tree_df,prob2calc):
    # if(tree_df[key].Parents)
    print("in..\n")
    
    # for indx,key in enumerate(prob2calc):
    #     # if node has parents split possible key per parent
    #     if(len(tree_df[key].Parents)!=0):
    #         parents_combinations = list(tree_df[key].CPT.keys())[0].split(',')

        # print(parents_combinations)
        # print(prob2calc[key])
        p = tree_df[key].CPT
        # print(tree_df[key].CPT[prob2calc[key]])


calculate_probs(df, prob2calc)
