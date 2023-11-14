#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tqdm
import time
from zipfile import ZipFile
import zipfile
import os
import spacy
import pandas as pd


# In[4]:


# only when gpu is available
spacy.require_gpu()


# In[5]:


# %%timeit -n 1 -r 1
nlp = spacy.load("en_core_web_trf")
# for spanish language dataset, use es_core_news_lg
#nlp = spacy.load("es_core_news_lg")



# In[67]:


def read_page(myfile, name, vol_id):
    """
    Read a HathiTrust scanned page given a myfile cursor (can be from compressed archive), name/path, and vol_id
    Return the extracted entities based on spacy language model nlp that has been loaded in the beginning of the script

    Args:
        myfile (file cursor): file cursor for a scanned page based on HathiTrust implementation
        name (string): file name or path (if it was read from a zip archive)
        vol_id (string): The name sometimes does not resemble the complete volume id so new parameter is added

    Returns:
        _type_: Return tuple of two items being the first item contains sentences on the page, and second item being the extracted ENTITY
    """

    # vol_id in the zip is not complete, replace it with the zip_name
    # by parameter

    # get volume_id and page_id
    _, page = name.split("/")
    # remove txt from page_id
    page = page.split(".")[0]
    # fixed page by only looking at the number

    sentence_ner = []
    sentence_id = 0
    temp_page = []
    for l in myfile:
        # print(l.decode("utf-8"))
        temp_page.append(l.decode("utf-8").strip())
    temp_page_str = " ".join(temp_page).replace("- ", "")  # .replace("\\n","")
    doc = nlp(temp_page_str)
    temp_sents = []
    for s in doc.sents:
        temp_sents.append((vol_id, page, sentence_id, str(s)))
        for eid, ts in enumerate(s.ents):
            sentence_ner.append((vol_id, page, sentence_id, eid, str(
                ts), ts.label_, ts.start_char-s.start_char, ts.end_char-s.start_char))
        sentence_id += 1
    return temp_sents, sentence_ner


# In[68]:


# read zip data
#!ls scwared_data


# In[73]:


# In[75]:

# start_time = time.time()
for f_name in tqdm.tqdm(os.listdir("scwared_data")):
    if f_name.endswith(".zip"):
        vol_id = ".".join(f_name.split(".")[:-1])
        if os.path.exists(f"result_output/{vol_id}.csv"):
            # skip if output exists
            continue
        # print(vol_id)
        # prepare a result list to store all entity objects for a volume
        result = []
        with ZipFile(f"scwared_data/{f_name}") as myzip:
            for temp_name in myzip.infolist():
                # print(temp_name.filename)
                with myzip.open(temp_name.filename) as myfile:
                    rr = read_page(myfile, temp_name.filename, vol_id)
                    result.extend(rr[1])
                    # break
        # break

        # render the list into dataframe
        result_pd = pd.DataFrame(result, columns=["vol_id", "page",
                                                  "sentence_id", "ent_id", "entity",
                                                  "entity_type", "start_char", "end_char"]). \
            sort_values(["page", "sentence_id", "ent_id"]
                        ).reset_index(drop=True)

        # save the result file as CSV, that result in a single NER  csv file for a volume 
        result_pd.to_csv(f"result_output/{vol_id}.csv", index=False)
# end_time = time.time()
# print(f"progress {end_time-start_time}")


# In[79]:


# result_pd = pd.DataFrame(result).sort_values(1).reset_index(drop=True)


# In[81]:


# result_pd[5].unique()
