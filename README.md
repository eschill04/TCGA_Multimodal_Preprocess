# Preprocessing for TCGA Datasets (End Stage)
Pipeline to permanently assign Case IDs to training, testing, and validation categories, then move the raw data from `.svs` and `.csv` file format to preprocessed tensors split via the pre-assigned IDs. 

### 1. Preprocess the non-image modalities

Run create_<modality>_dataset.ipynb for all four of the non-image modalities. This will organize the data in .csv form and perform some preliminary data cleaning such as dropping columns with NaN values and selecting highly variable features.

### 2. Assign Case IDs to train, test, and validate

Run `gen_splits_by_id.py` with the appropriate `DATA_PATH` and `ORGANIZED_BY_CASE_PATH`. This will select out any Case IDs which either do not have an image in `DX` format, or do not exist for one or more of the modalities. It then assign 75% of the remaning data to training, and 12.5% to testing and validation respectively. These assignments are shuffled, then saved them to a `.csv` file at your specified `ID_PATH`.

### 3. Preprocess and split the image modality

Run `create_image_dataset.py` with the appropriate `ID_PATH`, `SAVE_PATH`, and `ORGANIZED_BY_CASE_PATH`. This will select the image in `DX` format for each case, resize it to the median aspect ratio, and save it as a `.jpg` file to a subdirectory labeled `image_test`, `image_train`, or `image_val`.

### 4. Split non-image modalities into train, test, and validate

Run `ttv_split.py` with the appropriate `DATA_PATH`, `SAVE_PATH`, and `ID_PATH`. This will
produce three separate `.csv` files for each non-image modality, one for training, testing, and validation. The split is based on our pre-specified categorization of each Case ID. 

### 5. Feature reduction of larger datasets

Run `feature_reduction.py` with the appropriate `DATA_PATH` and `SAVE_PATH` to perform 
feature reduction via random forest classifier on the three larger modalities (DNA methylation, gene expression, and CNV). 

### 6. Create and save a custom tensor dataset for each modality

Run `tensor_convert.py` with the appropriate `DATA_PATH` and `SAVE_PATH` to create custom
datasets for all five modalities and save them as `.pt` files. 




