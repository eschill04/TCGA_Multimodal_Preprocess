import random
import pandas as pd
 
save_path = "/gpfs/data/rsingh47/eschill4_multimodal_data/shuffled_data/"
id_path = "/gpfs/data/rsingh47/eschill4_multimodal_data/id_ttv_split_shuffled.csv"
# read in ids and data
id_df = pd.read_csv(id_path)
ids = id_df["id"].tolist()
categories = id_df["cat"].tolist()
modalities = ["transcriptomic", "cnv", "epigenomic", "clinical"]
for modality in modalities:
    data = pd.read_csv("/gpfs/data/rsingh47/TCGA_Data/project_LUAD/data_processed/PRCSD_"+modality+"_data.csv")
    
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
    train.to_csv(save_path + modality+"_train.csv", index=False)
    test.to_csv(save_path + modality+"_test.csv", index=False)
    val.to_csv(save_path + modality+"_val.csv", index=False)


