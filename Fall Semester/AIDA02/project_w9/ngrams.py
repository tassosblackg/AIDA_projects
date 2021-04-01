# NLTK lib project on N-grams
# Week 9 ML&NLP
# author: @tassosblackg
import nltk
from nltk.corpus import gutenberg as gut
from nltk.text import Text
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.util import ngrams,trigrams,bigrams
import random
from nltk.probability import ConditionalFreqDist as CFD

# ----------------
#   Question A
# ----------------
# Get all books' titles of Gutenberg Corpus
books = gut.fileids()
# print(books,len(books))
# keep only the first Ten of them
books_10 = books[0:10]
print("\nFirst 10 Books Titles: \n",books_10)


# ----------------
#   Question B
# ----------------
# Keep whole text of 10 books into a list
book_full_txt = []
for i in books_10:
    book_txt = gut.raw(i)
    book_full_txt.append(book_txt)

# Creates a list of ten different vocabularies for each book
vocabulary_per_book,vocabulary_final,books_all_words = [],[],[]
for book_txt in book_full_txt:
    words_of_book = word_tokenize(book_txt) # split text to words
    books_all_words += words_of_book # keep all books words in a list
    vocabulary_per_book += set(words_of_book) # add list of unique words per book
# remove dublicate words between books
vocabulary_final += set(vocabulary_per_book)

print("\n Length of Vocaboluary as merged words from each book = ",len(vocabulary_per_book))
print("\n Length of vocabulary after removing dublicate words beetween books = ",len(vocabulary_final))

# ------------------
#     Question C
# ------------------
sentences = []
token = '<s>'
for book_txt in book_full_txt:
    for sent in sent_tokenize(book_txt):
        new_sentence = token+sent+token
    sentences.append(new_sentence)
# print("The number of total sentences is", len(sentences))
# print(sentences)

# ------------------
#     Question D
# ------------------
books_words_unigram = ngrams(books_all_words, 1, pad_left=True, pad_right=True, left_pad_symbol=token, right_pad_symbol=token)
unigram_fd = nltk.FreqDist(books_words_unigram)
# print(unigram_fd.keys())

bigrams =ngrams(books_all_words, 2, pad_left=True, pad_right=True, left_pad_symbol=token, right_pad_symbol=token)
bigram_fd = CFD(bigrams)
# print(bigram_fd.keys())


trigrams = ngrams(books_all_words, 3, pad_left=True, pad_right=True, left_pad_symbol=token, right_pad_symbol=token)
pairsOf3 = (((w0, w1), w2) for w0, w1, w2 in trigrams) # create tuple of words -trigrams and Calcualte CFD
trigram_fd = CFD(pairsOf3)
# print(trigram_fd.keys())


# print(Text(pairsOf3).generate(length=15))

# ------------------
#     Question E
# ------------------
# peek a random word and generate 10 sentences
def generate_model(cfdist, word, num=15,file_n):
    line = []
    line.append(word)
    for i in range(num):
        words = list(cfdist[word])
        word = random.choice(words)
        # print(word,file=open('output.txt', 'a'))
        line.append(word)
        # print(line)
    with open(file_n, 'a') as f:
        f.write(str(line)+'\n')

for i in range(0,10):
    generate_model(bigram_fd, '<s>', num=15,'bigram_senteces.txt')

# for i in range(0,10):
#     generate_model(trigram_fd, '<s>', num=15,'trigram_senteces.txt')
