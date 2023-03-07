import pandas as pd
import torch 
from torch.utils.data import Dataset, DataLoader
import matplotlib.image as mpimg
import numpy as np


DATA_PATH = "../../../eschill4_multimodal_data/shuffled_data/" 
SAVE_PATH = "../../../eschill4_multimodal_data/tensor_data/" 
ID_PATH = "../../../eschill4_multimodal_data/id_ttv_split_shuffled.csv"
id_order = pd.read_csv(ID_PATH) 

modalities_to_convert = ["cnv", "epigenomic", "transcriptomic", "clinical"] 
sets = ["train", "test", "val"]

'''
Custom Dataset used for all non-image modalities.
'''
class CSVDataset(Dataset):

    def __init__(self, m, s):

        # solutions
        self.sols = pd.read_csv(DATA_PATH +  "clinical_" + s + ".csv")["vital_status_Dead"].tolist()
        
        #data
        self.data = pd.read_csv(DATA_PATH + m + "_" + s + ".csv")
        
        # drop solutions and case ids
        case = "case_id"
        if(m == "clinical"):
            self.data = self.data.drop(columns=["vital_status_Dead"])
        self.data = self.data.drop(columns=[case])
        

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if isinstance(idx, torch.Tensor):
            idx = idx.tolist()
        return [self.data.iloc[idx].values, self.sols[idx]]
        

'''
Custom Dataset used for image modalities.
'''
class IMGDataset(Dataset):

    def __init__(self, arr, s):

        # solutions
        self.sols = pd.read_csv(DATA_PATH +  "clinical_" + s + ".csv")["vital_status_Dead"].tolist()
        
        #data
        self.data = arr
        

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return [self.data[idx], self.sols[idx]]

        

'''
Code to create and save non-image modalities
'''

for m in modalities_to_convert:
    for s in sets:
        dataset = CSVDataset(m, s)
        print(dataset)
        torch.save(dataset, SAVE_PATH + m + "_" + s + "_inputs.pt")

'''
Code to create and save image modality
'''

ids = id_order["id"].tolist()
cat = id_order["cat"].tolist()

lens = [360, 71, 71]

for s in range(0, 3):
    img_array = np.empty([lens[s], 650, 500, 3])
    idx = 0
    for i in range(0, len(ids)):
        case_id = ids[i]
        case_cat = cat[i]
        if case_cat == s:
            try: 
                image = mpimg.imread(DATA_PATH + "image_" + sets[s] + "/" + case_id + ".jpeg")
                img_array[idx] = image
            except:
                print(case_id, "not here")
            idx = idx + 1
    print(img_array.shape)
    dataset1 = IMGDataset(img_array, sets[s])
    torch.save(dataset1, SAVE_PATH + "image_"+ sets[s] + "_inputs.pt")
        
    
        
    
        
        
        
        
        
        
        
