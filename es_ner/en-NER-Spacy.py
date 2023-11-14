#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd
import os
import zipfile
from zipfile import ZipFile
import time
import torch


# In[2]:
if torch.cuda.is_available():
    # only when gpu is available
    print("CUDA is available, running Spacy with GPU")
    spacy.require_gpu()



#%%timeit -n 1 -r 1
nlp = spacy.load('model/en_core_web_trf-3.3.0')
nlp.add_pipe("sentencizer",before="transformer")


def read_page(myfile,name,vol_id):
    # get volume_id and page_id
    _, page = name.split("/")
    # remove txt from page_id
    page = page.split(".")[0]
    # fixed page by only looking at the number
    page = page[-8:]

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




# In[13]ls -ltr:

get_ipython().system('mkdir scwared-spanish-enmodel')


# In[ ]:


import tqdm

#start_time = time.time()

for l_dir in os.listdir("scwared-spanish-data"):
    if not os.path.isdir(f"scwared-spanish-data/{l_dir}"):
        continue
    get_ipython().system('mkdir scwared-spanish-enmodel/{l_dir}')
    for f_name in tqdm.tqdm(os.listdir(f"scwared-spanish-data/{l_dir}")):
        # skip if entity already exists
        result = []
        sentences = []
        vol_id = ".".join(f_name.split(".")[:-1])
        if os.path.exists(f"scwared-spanish-enmodel/{l_dir}/{vol_id}.csv"):
            continue
        if f_name.endswith(".zip"):
            with ZipFile(f"scwared-spanish-data/{l_dir}/{f_name}") as myzip:
                for temp_name in myzip.infolist():
                    #print(temp_name.filename)
                    with myzip.open(temp_name.filename) as myfile:
                        rr  = read_page(myfile,temp_name.filename,vol_id)
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
        result_pd.to_csv(f"scwared-spanish-enmodel/{l_dir}/{vol_id}.csv",index=False)