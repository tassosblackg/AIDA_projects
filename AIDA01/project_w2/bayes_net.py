import pandas as pd

df = pd.read_json("input.json")
tree_nodes = df.columns[df.columns!='ProblemName']
print(tags_nodes)
# Parse node data
for i in tree.nodes:
    print(df[i].Parents)
    print(df[i].CPT)

prob2calc = {"A":'True'} # {"A":'True','B':'False'}
#list(df.B.CPT.keys())[0].split(',') #-> get Parents values,for an evident
def calculate_probs(tree_df,prob2calc):
    #bn_joint_prob =
    pass
