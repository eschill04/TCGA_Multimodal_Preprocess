import pandas as pd
 
DATA_PATH = "PATH_TO_DATA"
SAVE_PATH = "PATH_TO_SAVE_DATA"
ID_PATH = "PATH_TO_ID_SPLIT"


id_df = pd.read_csv(ID_PATH)
ids = id_df["id"].tolist()
categories = id_df["cat"].tolist()
modalities = ["transcriptomic", "cnv", "epigenomic", "clinical"]

'''
Loop through modalities and read in data and create new DataFrames for train, test, and validate.
Using id_df (a mapping of Case IDs to train, test, and validate), sort columns between
the three groups and save the new csv's to SAVE_PATH.
'''
for modality in modalities:
    data = pd.read_csv(DATA_PATH + "PRCSD_" + modality + "_data.csv")
    
    # create new DataFrames for ttv sets
    train = pd.DataFrame(columns = list(data.columns.values))
    test = pd.DataFrame(columns = list(data.columns.values))
    val = pd.DataFrame(columns = list(data.columns.values))
    
    id_name = "case_id"
    # For each case id:
    for i in range(0, len(ids)):
        case_id = ids[i]
        cat = categories[i]
    
        # access row of id in data and add row to corresponding dataframe
        if(cat == 0):
            newrow = data.loc[data[id_name] == case_id]
            train = train.append(newrow, ignore_index=True)
        elif(cat == 1):
            newrow = data.loc[data[id_name] == case_id]
            test = test.append(newrow, ignore_index=True)
        else:
            newrow = data.loc[data[id_name] == case_id]
            val = val.append(newrow, ignore_index=True)
            
    # Save new dataframes as csvs
    train.to_csv(SAVE_PATH + modality+"_train.csv", index=False)
    test.to_csv(SAVE_PATH + modality+"_test.csv", index=False)
    val.to_csv(SAVE_PATH + modality+"_val.csv", index=False)


