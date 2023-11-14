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
#nlp = spacy.load('./es_model_com/model-best')
#nlp.add_pipe("sentencizer",before="transformer")
#nlp.remove_pipe("transformer")
#nlp.remove_pipe("ner")

nlp_en = spacy.load('en_core_web_trf')
nlp_en.add_pipe("sentencizer",before="transformer")


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
        #temp_page.append(l.decode("iso-8859-1").strip())
        #temp_page.append(l.strip())
        #temp_page.append(str(l).strip())
    temp_page_str = " ".join(temp_page).replace("- ","") #.replace("\\n","")
    #print(temp_page_str)
    doc = nlp_en(temp_page_str)
    temp_sents = []
    for s in doc.sents:
        #temp_sents.append((vol_id,page,sentence_id,str(s)))
        # replace sentence document with en ner transformer
        #s = nlp_en(str(s))
        for eid,ts in enumerate(s.ents):
            #sentence_ner.append((vol_id,page,sentence_id,eid,str(ts),ts.label_,ts.start_char,ts.end_char))
            sentence_ner.append((vol_id,page,sentence_id,eid,str(ts),ts.label_,ts.start_char,ts.end_char,str(s)))
        #for eid,ts in enumerate(s.ents):
        #    sentence_ner.append((vol_id,page,sentence_id,eid,str(ts),ts.label_,ts.start_char-s.start_char,ts.end_char-s.start_char))
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


get_ipython().system('mkdir scwared-spanish-custom-en')


# In[ ]:


import tqdm

#start_time = time.time()

for l_dir in os.listdir("scwared-spanish-data"):
    get_ipython().system('mkdir scwared-spanish-custom-en/{l_dir}')
    for f_name in tqdm.tqdm(os.listdir(f"scwared-spanish-data/{l_dir}")):
        # target only 4 documents for qa
        #files = ["mdp.39015056814810.zip","txu.059173025282111.zip","txu.059173027958890.zip","hvd.hnlhsz.zip"]
        
        files = ["hvd.hnleep.zip",
                "ien.35556034377929.zip",
                "mdp.39015062914646.zip",
                "pst.000009472877.zip",
                "txu.059173022904226.zip"]
        
        #files = ["pst.000009472877.zip"]
        #print(f_name)
        if f_name not in files:
            continue
        #print(f_name)

        # skip if entity already exists
        result = []
        sentences = []
        vol_id = ".".join(f_name.split(".")[:-1])
        #if os.path.exists(f"scwared-spanish-custom-en/{l_dir}/{vol_id}.csv"):
        #    continue
        
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
        

        """
        for temp_name in os.listdir("/N/u/ninoparu/Carbonate/slate/projects/scwared-ner/000009472877"):
            with open("/N/u/ninoparu/Carbonate/slate/projects/scwared-ner/000009472877/"+temp_name,encoding="utf-8") as myfile:
                rr  = read_page(myfile,"000009472877/"+temp_name)
                result.extend(rr[1])
                sentences.extend(rr[0])
        """

        result_pd = pd.DataFrame(result,columns=["vol_id","page", \
                                     "sentence_id","ent_id","entity", \
                                     "entity_type","start_char","end_char","sentence"]). \
                    sort_values(["page","sentence_id","ent_id"]).reset_index(drop=True)
        result_pd.to_csv(f"scwared-spanish-custom-en/{l_dir}/{vol_id}.csv",index=False)
        sentences_pd = pd.DataFrame(sentences, columns=["vol_id","page","sentence_id","sentence"]). \
            sort_values(["page","sentence_id"]).reset_index(drop=True)
        sentences_pd.to_csv(f"scwared-spanish-custom-en/{l_dir}/sent-{vol_id}.csv",index=False)        
#end_time = time.time()
#print(f"progress {end_time-start_time}")


# %%
