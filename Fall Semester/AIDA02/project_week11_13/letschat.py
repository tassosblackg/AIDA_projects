import json
import glob
import random
import csv
import os
import re
import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers , activations , models , preprocessing,utils
from tensorflow.keras.models import load_model
# from gensim.models import Word2Vec

# Data path / Files
data_path = "metalwoz-v1/dialogues/*.txt"
files_list = glob.glob(data_path) # get all files' names
print(files_list[:5],"Num of files = ",len(files_list))


def read_metalwozQA(files_list):
    '''
        Get a list with all files read it and split data to useful info
        Returns: Questions and Anwsers lists  (q,a)
    '''
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
    print("\n |> MetalWOz dataset read and splitted..finished!\n")

    return q,a

def save2tsv(q,a):
    '''
        Gets as input two lists one with (q)uestions & one with (a)nswers
        Output: save questions and answers pairs to .tsv file
    '''
    print('\n ..... creating .tsv data file .... \n')
    # save2file
    filepath2save = 'output.tsv'
    if (os.path.exists(filepath2save)):
        os.remove(filepath2save)
    with open(filepath2save, 'a') as f:
        writer = csv.DictWriter(f, delimiter='\t',fieldnames=["Questions","Answers"])
        writer.writeheader()
        tsv_writer = csv.writer(f, delimiter='\t') # tab separated entries
        # write
        for i in range(len(q)):
            tsv_writer.writerow([q[i], a[i]])
    print("\n |> QA pairs data created... ",filepath2save," is ready!\n")


def tokenize( sentences ):
    tokens_list = []
    vocabulary = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub( '[^a-zA-Z]', ' ', sentence )
        tokens = sentence.split()
        vocabulary += tokens
        tokens_list.append( tokens )
    return tokens_list , vocabulary


def make_inference_models():

    encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

    decoder_state_input_h = tf.keras.layers.Input(shape=( 200 ,))
    decoder_state_input_c = tf.keras.layers.Input(shape=( 200 ,))

    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_embedding , initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = tf.keras.models.Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return encoder_model , decoder_model


def str_to_tokens( sentence : str ):
    words = sentence.lower().split()
    tokens_list = list()
    for word in words:
        tokens_list.append( tokenizer.word_index[ word ] )
    return preprocessing.sequence.pad_sequences( [tokens_list] , maxlen=maxlen_questions , padding='post')


# ---------------------------------- Execution Part ----------------------------------------------
# |Important!!| Run only once to Format initial Data

# --- Step 0 - only once

# q,a = read_metalwozQA( files_list )
# save2tsv(q,a)

# -----

# --- Step 1 - Load Data as dataFrame
total_raws = 238051
df = pd.read_csv('output.tsv',sep='\t',nrows=1000) # a csv like format with headers Questions , Answers
print("\n \> Questions column-data ../\n",df.Questions)
print(df.Questions[1],type(df.Questions[1]))

answers_with_tags = [] # answers with start and end tag in each sentence
for answer in df.Answers :
    answers_with_tags.append( '<START> ' + answer + ' <END>' )
print("\n @ Answer without tags --> ",df.Answers[1])
print('\n @ Answer with tags check --> ',answers_with_tags[1])

questions = list(df.Questions)
# Tokenizing sentences
tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts( questions + answers_with_tags )
VOCAB_SIZE = len( tokenizer.word_index )+1
print( 'VOCAB SIZE : {}'.format( VOCAB_SIZE ))

# Prepare data for Seq2Seq model
# Get embendings using Word2Vec
vocab = []
for word in tokenizer.word_index:
    vocab.append( word )


# encoder_input_data
tokenized_questions = tokenizer.texts_to_sequences( questions )
maxlen_questions = max( [ len(x) for x in tokenized_questions ] )
padded_questions = preprocessing.sequence.pad_sequences( tokenized_questions , maxlen=maxlen_questions , padding='post' )
encoder_input_data = np.array( padded_questions )
print( encoder_input_data.shape , maxlen_questions )

# decoder_input_data
tokenized_answers = tokenizer.texts_to_sequences( answers_with_tags )
maxlen_answers = max( [ len(x) for x in tokenized_answers ] )
padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=maxlen_answers , padding='post' )
decoder_input_data = np.array( padded_answers )
print( decoder_input_data.shape , maxlen_answers )

# decoder_output_data
tokenized_answers = tokenizer.texts_to_sequences( answers_with_tags )
for i in range(len(tokenized_answers)) :
    tokenized_answers[i] = tokenized_answers[i][1:]
padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=maxlen_answers , padding='post' )
onehot_answers = utils.to_categorical( padded_answers , VOCAB_SIZE )
decoder_output_data = np.array( onehot_answers )
print( decoder_output_data.shape )

# Encoder Architecture
encoder_inputs = tf.keras.layers.Input(shape=( maxlen_questions , ))
encoder_embedding = tf.keras.layers.Embedding( VOCAB_SIZE, 200 , mask_zero=True ) (encoder_inputs)
encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 200 , return_state=True )( encoder_embedding )
encoder_states = [ state_h , state_c ]

# Decoder Arcitecture
decoder_inputs = tf.keras.layers.Input(shape=( maxlen_answers ,  ))
decoder_embedding = tf.keras.layers.Embedding( VOCAB_SIZE, 200 , mask_zero=True) (decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM( 200 , return_state=True , return_sequences=True )
decoder_outputs , _ , _ = decoder_lstm ( decoder_embedding , initial_state=encoder_states )
decoder_dense = tf.keras.layers.Dense( VOCAB_SIZE , activation=tf.keras.activations.softmax )
output = decoder_dense ( decoder_outputs )

# Synthesize model Autoencoder
model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output )
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='categorical_crossentropy')

model.summary() # summary of the model params,architecture
utils.plot_model(model) # model architecture

# #Train model
# model.fit([encoder_input_data , decoder_input_data], decoder_output_data, batch_size=50, epochs=150 )
# # model.save( 'model8k1.h5' ) # save trained model
# #
# # model = load_model('model8k1.h5')
# enc_model , dec_model = make_inference_models()
#
#
# # Talk with bot
# for _ in range(10):
#     states_values = enc_model.predict( str_to_tokens( input( 'Enter question : ' ) ) )
#     empty_target_seq = np.zeros( ( 1 , 1 ) )
#     empty_target_seq[0, 0] = tokenizer.word_index['start']
#     stop_condition = False
#     decoded_translation = ''
#     while not stop_condition :
#         dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + states_values )
#         sampled_word_index = np.argmax( dec_outputs[0, -1, :] )
#         sampled_word = None
#         for word , index in tokenizer.word_index.items() :
#             if sampled_word_index == index :
#                 decoded_translation += ' {}'.format( word )
#                 sampled_word = word
#
#         if sampled_word == 'end' or len(decoded_translation.split()) > maxlen_answers:
#             stop_condition = True
#
#         empty_target_seq = np.zeros( ( 1 , 1 ) )
#         empty_target_seq[ 0 , 0 ] = sampled_word_index
#         states_values = [ h , c ]
#
#     print( decoded_translation )
