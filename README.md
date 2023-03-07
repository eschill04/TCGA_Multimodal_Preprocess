# Preprocessing for TCGA Datasets (End Stage)

### 1. Preprocess the image modality

Run img_process.py with the appropriate ID_PATH, SAVE_PATH, and ORGANIZED_BY_CASE_PATH. This will identify all Case IDs with an image of 'DX' format, resize them to the median aspect ratio, and save them as .jpg files to folders labeled 'image_test', 'image_train', and 'image_val'.

### 2. Split non-image modalities into train, test, and validate

Run ttv_split.py with the appropriate DATA_PATH, SAVE_PATH, and ID_PATH. This will
produce three separate .csv files for each non-image modality, one for training, testing, and validation. The split is based on our pre-specified categorization of each Case ID. 

### 3. Feature reduction of larger datasets

Run feature_reduction.py with the appropriate DATA_PATH and SAVE_PATH to perform 
feature reduction via random forest classifier on the three larger modalities (DNA methylation, gene expression, and CNV). 

### 4. Create and save a custom tensor dataset for each modality

Run tensor_convert.py with the appropriate DATA_PATH and SAVE_PATH to create custom
datasets for all five modalities and save them as .pt files. 




