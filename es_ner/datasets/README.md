# ES Spacy custom model training pipeline

Make sure you have the environment setup in a proper GPU environment for training pipelines.

1. Activate  the environment
```
conda activate spacy-cuda117
```

2. Make sure the anaconda environment is active by looking at the bash prompt, it should mentioned the environment like this
```
(spacy-cuda117) [someuser@somesystem en_ner]$
```

3. You can run the dataset preprocessor on Jupyter notebook or run the Python version using "ipython"
```
ipython dataset_preprocessor.py
```
This will read and combines all the Spanish NER datasets we have collected and split the data into training, test, and eval sets in IOB format. The script then will transfom those generated sets into spacy format. In the end the script will have three files train.spacy, test.spacy, and val.spacy

4. once the datasets is ready we can run spacy training using config "es_run_config.cfg"
```
python -m spacy train -g 0 es_run_config.cfg --output ./es_output --paths.train train.spacy --paths.dev test.spacy
```
This will run the spacy training pipelines on GPU 0 and save the output on the es_output folder. The training will be lasting for maximum 2 epochs that can be set on the es_run_config.cfg or using running parameter.
