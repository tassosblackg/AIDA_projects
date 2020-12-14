# NLTK lib project on N-grams
# Week 9 ML&NLP
# author: @tassosblackg
import nltk
from nltk.corpus import gutenberg as gut
from nltk.text import Text
from nltk.tokenize import sent_tokenize,word_tokenize


# Get all books' titles of Gutenberg Corpus
books = gut.fileids()
print(books,len(books))
# keep only the first Ten of them
books_10 = books[0:10]
print(books_10)



# Creates a lsit of ten different vocabularies for each book
vocabulary_per_book,vocabulary2 = [],[]
for i in books_10:
    # print(i)
    book_txt = gut.raw(i)
    words_of_book = word_tokenize(book_txt) # split text to words
    vocabulary_per_book += set(words_of_book) # add list of unique words per book
# remove dublicate words between books
vocabulary_final += set(vocabulary_per_book)

print("\n Length of Vocaboluary as merged words from each book = ",len(vocabulary_per_book))
print("\n Length of vocabulary after removing dublicate words beetween books = ",len(vocabulary_final))


# sents = nltk.sent_tokenize(list1)
# print("The number of sentences is", len(sents),type(sents))
# words = nltk.word_tokenize(list1)
# print("The number of tokens is", len(words),type(words))
# average_tokens = round(len(words)/len(sents))
# print("The average number of tokens per sentence is",average_tokens)
# unique_tokens = set(words)
# print("The number of unique tokens are", len(unique_tokens))
