import random
import pandas as pd
import os
 
# read DataFrame
DATA_PATH = "PATH_TO_DATA"
ORGANIZED_BY_CASE_PATH = "PATH_TO_DATA_BY_CASES"

'''
Get ids for non-image csv files
'''
clinical = pd.read_csv(DATA_PATH + "clinical_data.csv")
case_ids = clinical['case_id'].tolist()

#get cnv ids
cnv = pd.read_csv(DATA_PATH + "cnv_data.csv")
c_ids = cnv['case_id'].tolist()

#get epigenomic ids
epigenomic = pd.read_csv(DATA_PATH + "epigenomic_data.csv")
e_ids = epigenomic['case_id'].tolist()

#get transcriptomic ids
transcriptomic = pd.read_csv(DATA_PATH + "transcriptomic_data.csv")
t_ids = transcriptomic['case_id'].tolist()

'''
Find all cases with a DX image
'''
case_files = os.listdir(ORGANIZED_BY_CASE_PATH)
i_ids = []

for case in case_files:
    img_files = os.listdir(os.path.join(ORGANIZED_BY_CASE_PATH, case, "images"))
    for f in img_files:
        if (f.split('.')[0][-3:-1] == 'DX'):
            i_ids.append(case)

print(i_ids)

'''
Only keep ids that exist for every modality!
'''
safe_ids = []
in_all = True
for i in range(0, len(case_ids)):
    curr_id = case_ids[i]
    if curr_id not in c_ids:
        in_all = False
    if curr_id not in e_ids:
        in_all = False
    if curr_id not in t_ids:
        in_all = False
    if curr_id not in i_ids:
        in_all = False
    if in_all:
        safe_ids.append(curr_id)
    in_all = True


'''
Divide safe ids by vitality_status_Dead
'''

alive_ids = []
dead_ids = []
print(len(safe_ids))
for i in range(0, len(safe_ids)):
    vital_status = (clinical.loc[clinical['case_id'] == safe_ids[i]])["vital_status_Dead"].iloc[0]
    if vital_status == 0:
        alive_ids.append(safe_ids[i])
    else:
        dead_ids.append(safe_ids[i])

'''
Generate split locations for train, test, validate
'''

TRAIN_RATIO = 0.75
TEST_VAL_RATIO = 0.125

num_a = len(alive_ids)
num_d = len(dead_ids)

train_alive = round(num_a * TRAIN_RATIO)
train_dead = round(num_d * TRAIN_RATIO)
test_alive = round(num_a * TEST_VAL_RATIO)
test_dead = round(num_d * TEST_VAL_RATIO)
val_alive = num_a - train_alive - test_alive
val_dead = num_d - train_dead - test_dead


'''
Divide into train, test, and validation datasets, then add to a dictionary id_dict
'''
train = alive_ids[:train_alive] + dead_ids[:train_dead]
test = alive_ids[train_alive:train_alive + test_alive] + dead_ids[train_dead:train_dead + test_dead]
val = alive_ids[train_alive + test_alive:train_alive + test_alive + val_alive] + dead_ids[train_dead + test_dead:train_dead + test_dead + val_dead]

id_dict = {}
for i in train:
    id_dict[i] = 0
for i in test:
    id_dict[i] = 1
for i in val:
    id_dict[i] = 2

final_dict = {}
final_dict['id'] = id_dict.keys()
final_dict['cat'] = id_dict.values()
id_df = pd.DataFrame(final_dict)

'''
Shuffle the final dataframe and save to csv
'''
id_df = id_df.sample(frac = 1)
id_df.to_csv("id_ttv_split.csv", index = False)