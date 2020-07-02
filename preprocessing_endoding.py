import numpy as np
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from math import log, sqrt
import nltk
import string
import re
import spacy
##### Use USE pretrained model encode text
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text

nlp = spacy.load('en_core_web_sm')


def message_processing(mssg):  
    ## lower
    mssg = [w.lower() for w in mssg.split()]
    mssg = ' '.join(mssg)
    
    ## Remove Ponctuation
    mssg = [w for w in mssg if w not in string.punctuation or w == '-']
    mssg = ''.join(mssg)
    
    ## remove \n and \r
    mssg = mssg.replace('\n','').replace('\t','')

    ## remove multispaces
    mssg = re.sub(r'\s+', ' ', mssg)

    ## remove the question mark if it exists
    if( mssg[-1] == " "): mssg = mssg[:-1]
    if( mssg[-1] == "?"): mssg = mssg[:-1]
    
    ## remove non alphnum words
    mssg = ' '.join(e for e in mssg.split(' ') if (e.isalpha() or e == 'covid-19'))

    ## lemmetization
    doc = nlp(mssg)
    lemma_mssg = [token.lemma_ for token in doc if token.lemma_ != '-PRON-']
    
    return ' '.join(lemma_mssg)


## read data
data = pd.read_csv(r'all_data.csv').drop(columns=["Unnamed: 0"])

## preprocess the text
data['Question'] = data['Question'].apply(message_processing)
data['Answer'] = data['Answer'].apply(message_processing)

# Load module containing USE
module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')

# Create response embeddings
question_encodings1 = module.signatures['response_encoder'](
                    input=tf.constant(list(data.Question)[:100]),
                    context=tf.constant(list(data.Answer)[:100]))['outputs']

# Create response embeddings
question_encodings2 = module.signatures['response_encoder'](
                    input=tf.constant(list(data.Question)[100:200]),
                    context=tf.constant(list(data.Answer)[100:200]))['outputs']

# Create response embeddings
question_encodings3 = module.signatures['response_encoder'](
                    input=tf.constant(list(data.Question)[200:]),
                    context=tf.constant(list(data.Answer)[200:]))['outputs']

question_encodings_total = tf.concat([question_encodings1, question_encodings2,question_encodings3], 0)

# save this encoded text
np.save("response_encodings_total",question_encodings_total)
