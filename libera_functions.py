# Imports and Global Variables:

import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
import re
import string

stopword = stopwords.words('english')
stopword += ['.', ',','?','!','@', '(', ')', "'", "-",'"', ":","''","``",'facebook','ie','div','ffffff',
             'in','also','around','on','cx','like','it','would','go']
stopword = set(stopword)


# Webpage Processing Functions

def blog_tokenize(text, tokenizer, stemmer):
    """Tokenizes and stems words in a text doc
    Uses TreebankTokenizer and Porter Stemmer by default
    
    This function also removes words with numbers and underscores,
    eliminates punctuation, and returns all the words as lowercase"""
    text = text.lower()
    drop_patterns = ['[0-9_]','adblo','addservic','appendchild','imageresult','http','gs','gsc','getelement','ll',
                     'keyvaluepair','defineslot','customsearchcontrol','cmd','createel','googletag','setattr',
                     'setprop','parentnode']
    tokens = tokenizer.tokenize(text)
    tokens = [w for w in tokens if w not in stopword]
    for string in drop_patterns:
        drop_pattern = re.compile(string, re.I)
        tokens = [w for w in tokens if not drop_pattern.search(w)]
    stems  = stem_tokens(tokens, stemmer)
    return stems

def stem_tokens(tokens, stemmer):
    """Stems tokenized words, this function is called by tokenize which uses Porter Stemmer by default"""
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def preprocess_vectorize(text,tokenizer=TreebankWordTokenizer(), stemmer=PorterStemmer()):
    """Prepares a document for vectorizer transformation"""
    text_stemmed = []
    text_stemmed.append(blog_tokenize(text,tokenizer,stemmer))
    doc_list = [""]
    for word in text_stemmed:
	doc_list += word+" "
    return doc_list
