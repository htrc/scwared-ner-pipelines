#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd


# # AIJ dataset

# In[2]:


get_ipython().system('head aijwikinereswp2')


# In[3]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)
with open("aijwikinereswp2","r",encoding="ISO 8859-1") as file:
    sentences = []
    for l in file:
        sent = l.replace("\n","").split(" ")
        if sent != ['']:
            sentences.append(l.replace("\n","").split(" "))


# # only for wikiner, split train and test manually

# In[5]:


train_idx = int(.6 * len(sentences))
test_idx = int(.8 * len(sentences))


# In[6]:


len(sentences)


# In[7]:


train_list = []
test_list = []
val_list = []

f_name = "aijwikinereswp2"
sent_id = 0
for sent in sentences[:train_idx]:
    for t in sent:
        ent = t.split("|")
        train_list.append((t,f_name,sent_id,ent[0],ent[2]))
    #train_list.append(("",f_name))
    sent_id+=1

sent_id = 0
for sent in sentences[train_idx:test_idx]:
    for t in sent:
        ent = t.split("|")        
        test_list.append((t,f_name,sent_id,ent[0],ent[2]))
    sent_id+=1
    
sent_id = 0
for sent in sentences[test_idx:]:
    for t in sent:
        ent = t.split("|")        
        val_list.append((t,f_name,sent_id,ent[0],ent[2]))
    sent_id+=1


# In[8]:


pd.DataFrame(train_list).loc[:50]


# In[9]:


pd.DataFrame(train_list).groupby(1).count()


# # panx dataset

# In[10]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)
with open("es/train","r",encoding="ISO 8859-1") as file:
    sentences = []
    for l in file:
        #print(l)
        sent = l[3:].replace("\n","")#.split("\t")
        #if sent != ['']:
        sentences.append(sent)        


# In[11]:


f_name = "pannx"

sent_id = 0
for r in pd.read_csv("es/train",sep="\t",header=None,skip_blank_lines=False).to_records():
    if not pd.isna(r["0"]):
        token = "es:".join(r["0"].split("es:")[1:])
        train_list.append((r,f_name,sent_id,token,r["1"]))
    else:
        sent_id+=1
    

"""
sent_id = 0
for sent in sentences:
    ent = sent.split("\t")
    try:
        train_list.append((sent,f_name,sent_id,ent[0],ent[1]))
    except:
        pass
    if sent == "":
        sent_id+=1
    #train_list.append(("",f_name))
"""    


# In[12]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)
with open("es/test","r",encoding="ISO 8859-1") as file:
    sentences = []
    for l in file:
        #print(l)
        sent = l[3:].replace("\n","")#.split("\t")
        #if sent != ['']:
        sentences.append(sent)        


# In[13]:


f_name = "pannx"

sent_id = 0
for r in pd.read_csv("es/test",sep="\t",header=None).to_records():
    if not pd.isna(r["0"]):
        token = "es:".join(r["0"].split("es:")[1:])
        test_list.append((r,f_name,sent_id,token,r["1"]))
    else:
        sent_id+=1
    
"""
sent_id = 0
for sent in sentences:
    ent = sent.split("\t")
    try:
        test_list.append((sent,f_name,sent_id,ent[0],ent[1]))
    except:
        pass
    if sent == "":
        sent_id+=1
    #train_list.append(("",f_name))
"""    


# In[14]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)
with open("es/dev","r",encoding="ISO 8859-1") as file:
    sentences = []
    for l in file:
        #print(l)
        sent = l[3:].replace("\n","")#.split("\t")
        #if sent != ['']:
        sentences.append(sent)        


# In[15]:


f_name = "pannx"

sent_id = 0
for r in pd.read_csv("es/dev",sep="\t",header=None).to_records():
    if not pd.isna(r["0"]):
        token = "es:".join(r["0"].split("es:")[1:])
        val_list.append((r,f_name,sent_id,token,r["1"]))
    else:
        sent_id+=1
        
"""
sent_id = 0
for sent in sentences:
    ent = sent.split("\t")    
    try:
        val_list.append((sent,f_name,sent_id,ent[0],ent[1]))
    except:
        pass
    if sent == "":
        sent_id+=1
    #train_list.append(("",f_name))
"""    


# In[16]:


pd.DataFrame(train_list).groupby(1).count()


# # wikineural

# In[17]:


# preprocess wikineural dataset
label_token = {'O': 0, 'B-PER': 1, 'I-PER': 2, 'B-ORG': 3, 'I-ORG': 4, 'B-LOC': 5, 'I-LOC': 6, 'B-MISC': 7, 'I-MISC': 8}
label_id = {v:k for k,v in label_token.items()}
label_id


# In[18]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)

            
import json
with open("wikineural/train_es.jsonl","r") as file:
    sentences = []
    for l in file:
        jj = json.loads(l)
        tok = jj["tokens"]
        ner = [label_id[x] for x in jj["ner_tags"]]
        list_tok = list(zip(tok,ner))
        #sent = []
        #for x in list_tok:
        #    sent.append("{}".format(" ".join(x)))
        sentences.append(list_tok)


# In[19]:


f_name = "wikineural"
sent_id = 0
for sent in sentences:
    for t in sent:
        train_list.append((t,f_name,sent_id,t[0],t[1]))
    sent_id+=1


# In[20]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)

            
import json
with open("wikineural/test_es.jsonl","r") as file:
    sentences = []
    for l in file:
        jj = json.loads(l)
        tok = jj["tokens"]
        ner = [label_id[x] for x in jj["ner_tags"]]
        list_tok = list(zip(tok,ner))
        #sent = []
        #for x in list_tok:
        #    sent.append("{}".format(" ".join(x)))
        sentences.append(list_tok)


# In[21]:


f_name = "wikineural"
sent_id = 0
for sent in sentences:
    for t in sent:
        test_list.append((t,f_name,sent_id,t[0],t[1]))
    sent_id+=1


# In[22]:


# read aijwikinereswp
# UTF-8 does not work with this dataset (strange charset)

            
import json
with open("wikineural/val_es.jsonl","r") as file:
    sentences = []
    for l in file:
        jj = json.loads(l)
        tok = jj["tokens"]
        ner = [label_id[x] for x in jj["ner_tags"]]
        list_tok = list(zip(tok,ner))
        #sent = []
        #for x in list_tok:
        #    sent.append("{}".format(" ".join(x)))
        sentences.append(list_tok)


# In[23]:


f_name = "wikineural"
sent_id = 0
for sent in sentences:
    for t in sent:
        val_list.append((t,f_name,sent_id,t[0],t[1]))
    sent_id+=1


# In[24]:


pd.DataFrame(train_list).groupby(1).count()


# In[25]:


pd.DataFrame(train_list)


# In[26]:


pd.DataFrame(train_list)[[1,2,3,4]].groupby(1).max()


# # Randomize training set so neural network will not learn about dataset pattern

# In[27]:


train_rd = pd.DataFrame(train_list)


# In[28]:


train_rd.groupby([1,2]).count().index


# In[29]:


import random
random.seed(777)
random_index = list(train_rd.groupby([1,2]).count().index)
random.shuffle(random_index)


# In[30]:


random_index


# In[31]:


train_rdg = train_rd.groupby([1,2])


# In[32]:


# create IOB file
import tqdm

with open("train.iob","w",encoding="UTF-8") as file:
    for g in tqdm.tqdm(random_index):
        train_g = train_rdg.get_group(g)
        for r in train_g.to_records():
            #file.write(f"{r['3'].encode('UTF-8').decode('UTF-8')}\t{r['4'].encode('UTF-8').decode('UTF-8')}\n")
            file.write(f"{r['3']} {r['4']}\n")
        # space after one sentence
        file.write("\n")
    


# In[35]:


train_rd = pd.DataFrame(test_list)


# In[36]:


train_rdg = train_rd.groupby([1,2])


# In[37]:


# create IOB file
import tqdm

with open("test.iob","w") as file:
    for g in tqdm.tqdm(train_rdg.count().index):
        train_g = train_rdg.get_group(g)
        for r in train_g.to_records():
            file.write(f"{r['3']} {r['4']}\n")
        # space after one sentence
        file.write("\n")
    


# In[38]:


train_rd = pd.DataFrame(val_list)


# In[39]:


train_rdg = train_rd.groupby([1,2])


# In[40]:


# create IOB file
import tqdm

with open("val.iob","w") as file:
    for g in tqdm.tqdm(train_rdg.count().index):
        train_g = train_rdg.get_group(g)
        for r in train_g.to_records():
            file.write(f"{r['3']}\t{r['4']}\n")
        # space after one sentence
        file.write("\n")
    


# In[41]:


import locale


# In[44]:


get_ipython().system('wc -l *.iob')


# # convert into spacy datasets

# In[45]:


#!PYTHONIOENCODING="ISO 8859-1" python -m spacy convert -c iob -s -n 5 -t spacy train.iob .
get_ipython().system('python -m spacy convert -c iob -s -n 5 -t spacy train.iob .')


# In[46]:


get_ipython().system('python -m spacy convert -c iob -s -n 5 -t spacy test.iob .')


# In[47]:


#!PYTHONIOENCODING="ISO 8859-1" python -m spacy convert -c iob -s -n 5 -t spacy train.iob .
get_ipython().system('python -m spacy convert -c iob -s -n 5 -t spacy val.iob .')


# In[ ]:




