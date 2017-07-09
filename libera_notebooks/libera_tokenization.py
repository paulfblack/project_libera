from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
import re

stopword = stopwords.words('english')
stopword += list(string.punctuation)
stopword += ['``', '\'\'', '–','.','=',')','(',';','``']
stopword += ['january','february','march','april','may','june','july','august','september','october','november',
            'december','jan','feb','mar','apr','jul','aug','sep','oct','nov','dec', 'fadeoutdown',
             'fadeinup','getelementsbyclassname','serif','sans','answer','mon','tue','wed','thu','fri','sat','sun',
            'br','content','cdata','neue', 'helvetica','faq','feedplaceholdergroup','var','getelementsbyclassname',
             'js','parseparamsfromurl','function','follow','like','mouseout','need','share','tweet','email',
             'address', 'name', 'website','keyvaluepair','nvar','onloadfunctionsobj', 'createscripttagfunc',
            'subscribe','rss','queryparamname', 'urlparams','cbsigptdivids','np', 'xef', 'xbf', 'ntext',
             'numsources', 'encryptedtoken','usessl', 'https', 'promotion', 'gs', 'visibleurl', 'qe', 'xef', 'xbf',
            'searchclick', 'customprovider','customprovider','cx','ie','dtick','whitelabelsharing','setinterval',
             'tjquery','fileformattype','hover','buttonseffect','imageresult','span','customsearchoptions', 'th',
             'customsearchcontrol','clearinterval','queryparamname','want','webresult','isstorifyurl','arial',
             'border', 'color','background','blog', 'receive','notif','browser', 'facebook','check','font','display',
            'comment','commentform','contact','twitter','family','fieldset','googletag','permalink']

def tokenize(text_column, tokenizer=TreebankWordTokenizer(), stemmer=PorterStemmer()):
    """Tokenizes and stems words in a text doc
    Uses TreebankTokenizer and Porter Stemmer by default
    
    This function also removes words with numbers and underscores,
    eliminates punctuation, and returns all the words as lowercase
    """
    token_list = []
    for row in text_column:
        row = row.lower()
        pattern = re.compile('[^a-zA-Z-\' ]+|x\w{2,6}')
        tokens = tokenizer.tokenize(row)
        tokens_no_stopwords = [w for w in tokens if w not in stopword]
        tokens_dropped_patterns = [w for w in tokens_no_stopwords if not pattern.search(w)]
        stems  = stem_tokens(tokens_dropped_patterns, stemmer)
        blogs= ' '.join(stems)
        token_list.append(blogs)
    return token_list

def stem_tokens(tokens, stemmer):
    """Stems tokenized words, this function is called by tokenize which uses Porter Stemmer by default"""
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed
