# Spacy Entity Extraction for Spanish volumes

The pipeline was developed using (version 2020.07) on Linux with anaconda environment for Python
The extracted results from this project is using a custom spacy transformers model and others entity detection results using en_core_web_trf 3.3.0
The initial conda environment requirements can be found on conda-env-cuda117.yml
The additional pip requirements can be found on pip-env-cuda117.txt
We separate the two requirements to avoid dependency conflicts and make sure the environment is consistent on different system

1. If it doesn't exist yet, create anaconda environment tor run spacy transformers model using
```
conda env create -f conda-env-cuda117.yml
```
This will create a Python environment named spacy-cuda117 that will allow the extraction execution.
The environment will be perfectly running with NVIDIA GPU available and the cuda driver 11.7 installed to access the full power.
Otherwise, the environment should still be runnable with CPU only processing.

2. Activate  the environment
```
conda activate spacy-cuda117
```

3. Make sure the anaconda environment is active by looking at the bash prompt, it should mentioned the environment like this
```
(spacy-cuda117) [someuser@somesystem en_ner]$
```
In this activated cuda117 environment and install pip requirements by executing
```
pip install --no-deps -r pip-env-cuda117.txt
```
Make sure the --no-deps is included to force installation without looking at dependency since we are using a specific library required for cuda driver 11.7

4. The data should be placed on scwared-spanish-data folder. In this scwared spanish datasets, we also have categorized the input volumes into sub-genre where each datasets will be placed under the folder representing the sub-genre.
We used compressed zip format in this case as our input data. If one want to perform this pipeline on HTRC analytics data capsule, they can modified extraction scripts or compressed the volume folder into a zip where one zip represents one volume.

5. Run the extraction script using ipython for interactivity with the bash prompt, this will read all the zip files in the scwared_data folder and create a csv file in the scwared-spanish-custom folder for each sub-genre folder represented on the input folder.
```
ipython es-NER-Spacy.py
```
