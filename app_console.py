import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import re
import string
import spacy
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")
import string

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


## load encoded_reponses
print("please wait for a while !")
data = pd.read_csv(r'all_data.csv').drop(columns=["Unnamed: 0"])
encoded_reponses = np.load('Question_encodings_total.npy')
module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')
print("Ready to answer you questions !")

# Generating response
def response(user_response):

    question_encoding = module.signatures['question_encoder'](tf.constant(message_processing(user_response)))['outputs']
	# Get the responses
    test_responses = data.Answer[np.argmax(np.inner(question_encoding, encoded_reponses), axis=1)]
	# Show them in a dataframe
    #print("response : ", list(test_responses)[0])
    return list(test_responses)[0]

def chat(user_response):
    user_response=user_response.lower()


    if(user_response!='quit'):
        if(user_response=='thanks' or user_response=='thank you' ):


            return "You are welcome.."

        else:

            return response(user_response)
                #sent_tokensone.remove(user_response)
