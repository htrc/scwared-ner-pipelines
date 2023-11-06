#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd


# In[2]:
spacy.require_gpu()

# only when gpu is available
#spacy.require_gpu()


# In[5]:


#%%timeit -n 1 -r 1
nlp = spacy.load('./es_model_com/model-best')
nlp.add_pipe("sentencizer")

# In[6]:


def read_page(myfile,name):
    # get volume_id and page_id
    vol_id,page = name.split("/")
    # remove txt from page_id
    page = page.split(".")[0]
    sentence_ner = []
    sentence_id = 0
    temp_page = []
    for l in myfile:
        #print(l.decode("utf-8"))
        temp_page.append(l.decode("utf-8").strip())
    temp_page_str = " ".join(temp_page).replace("- ","") #.replace("\\n","")
    doc = nlp(temp_page_str)
    temp_sents = []
    for s in doc.sents:
        temp_sents.append((vol_id,page,sentence_id,str(s)))
        for eid,ts in enumerate(s.ents):
            sentence_ner.append((vol_id,page,sentence_id,eid,str(ts),ts.label_,ts.start_char-s.start_char,ts.end_char-s.start_char))
        sentence_id+=1
    return temp_sents,sentence_ner,vol_id


# In[7]:


# read zip data
#!ls scwared_data


# In[8]:


import os
import zipfile
from zipfile import ZipFile
import time


# In[13]:


get_ipython().system('ls scwared-spanish-data')


# In[12]:


get_ipython().system('mkdir scwared-spanish-custom')


# In[ ]:


import tqdm

#start_time = time.time()

for l_dir in os.listdir("scwared-spanish-data"):
    get_ipython().system('mkdir scwared-spanish-custom/{l_dir}')
    for f_name in tqdm.tqdm(os.listdir(f"scwared-spanish-data/{l_dir}")):
        # skip if entity already exists
        result = []
        sentences = []
        vol_id = ".".join(f_name.split(".")[:-1])
        if os.path.exists(f"scwared-spanish-custom/{l_dir}/{vol_id}.csv"):
            continue
        if f_name.endswith(".zip"):
            with ZipFile(f"scwared-spanish-data/{l_dir}/{f_name}") as myzip:
                for temp_name in myzip.infolist():
                    #print(temp_name.filename)
                    with myzip.open(temp_name.filename) as myfile:
                        rr  = read_page(myfile,temp_name.filename)
                        result.extend(rr[1])
                        sentences.extend(rr[0])
                        #break
            #break
                #with myzip.open('eggs.txt') as myfile:
                #    print(myfile.read())
            #break
        result_pd = pd.DataFrame(result,columns=["vol_id","page", \
                                     "sentence_id","ent_id","entity", \
                                     "entity_type","start_char","end_char"]). \
                    sort_values(["page","sentence_id","ent_id"]).reset_index(drop=True)
        result_pd.to_csv(f"scwared-spanish-custom/{l_dir}/{vol_id}.csv",index=False)
        sentences_pd = pd.DataFrame(sentences, columns=["vol_id","page","sentence_id","sentence"]). \
            sort_values(["page","sentence_id"]).reset_index(drop=True)
        sentences_pd.to_csv(f"scwared-spanish-custom/{l_dir}/sent-{vol_id}.csv",index=False)        
#end_time = time.time()
#print(f"progress {end_time-start_time}")

