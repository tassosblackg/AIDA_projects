import json
import glob
import random
import csv
import os
# from operator import itemgetter as ig

# data path
data_path = "metalwoz-v1/dialogues/*.txt"
files_list = glob.glob(data_path) # get all files' names
print(files_list[:5],"Num of files = ",len(files_list))

# parser of data
raw_data = []   # list of dictionaries
for file_i in files_list:   # for each file name
    with open(file_i) as f: # open file
        for line in f:
            raw_data.append(json.loads(line)) # append line readed as json

#check data
print("\n@ Data type of (",type(raw_data[0]),") \n content ->",raw_data[0])
print(raw_data[0].keys)

# Filter Input Data
turns_dlist = [] # list of dictionaries with only pairs -> ("turns":sentences)

for d in raw_data:
    # split dictionary to pairs (key,value) and get "turns": value
    qa =  {key:value for key, value in d.items() if key == "turns"}
    # append mixed (q)uestions and (a)nswers to qa list
    turns_dlist.append(qa) # list of dictionaries

# first_turn = list(map(ig('turns'),turns_dlist))
print(turns_dlist[100],"\n len_sent= ", len(turns_dlist[100]['turns']))
print("\nNum of Turns-mixed = ", len(turns_dlist))

'''
!Notice: that questions and answers are mixed inside the dictionary value
bot starts and ends the conversation
also the length of each 'turns'/key's, value-list size is not equal
'''

# Triggering start and end of conversation

greetings = ["Hey","Hi","Eoo"]
closings = ["Thanks","Bye","Okk"]

q, a =[],[]
count = 0

# all_topics_sentences = list(map(ig('turns'),turns_dlist))

for d in turns_dlist:
    all_topics_sentences = d['turns']

    q.append(random.choice(greetings)) # choose a greting as start of questions-init

    '''
    (*) Suppose the first sentence in each turns' value is from the bot, so each a # QUESTION:
    then the following one is from the user so we split them by pairs and append them to list
    but not always bot opens and close the conversation.
    '''

    # append like forward-backward from bot to user
    # aka answers to questions
    answering = True # bot talking state

    for sentence in all_topics_sentences:

        if answering: # it's bot turn
            a.append(sentence)
            answering = False
            continue
        else:   # it's user turn
            q.append(sentence)
            answering = True
            continue

    # if previously/last sentence was from user
    if answering:
        a.append(random.choice(closings))

# same length
print(len(q),len(a))


# save2file
filepath_to_save = 'output.tsv'
if (os.path.exists(filepath_to_save)):
    os.remove(filepath_to_save)
with open(filepath_to_save, 'a') as f:
    writer = csv.DictWriter(f, delimiter='\t',fieldnames=["Questions","Answers"])
    writer.writeheader()
    tsv_writer = csv.writer(f, delimiter='\t') # tab separated entries
    # write
    for i in range(len(q)):
        tsv_writer.writerow([q[i], a[i]])
