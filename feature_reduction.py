import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

modalities = ["cnv", "transcriptomic", "epigenomic"]
access_path = "/gpfs/data/rsingh47/eschill4_multimodal_data/shuffled_data/nonreduced/"
save_path = "/gpfs/data/rsingh47/eschill4_multimodal_data/shuffled_data/"

for modality in modalities:
    train = pd.read_csv(access_path + modality + "_train.csv")
    test = pd.read_csv(access_path + modality + "_test.csv")
    val = pd.read_csv(access_path + modality + "_val.csv")
    
    case = "case_id"
        
    X_train = train.drop(columns=[case])
    clinical = pd.read_csv("/gpfs/data/rsingh47/eschill4_multimodal_data/shuffled_data/clinical_train.csv")
    y_train = clinical['vital_status_Dead']
    
    sel = SelectFromModel(RandomForestClassifier(n_estimators = 100))
    sel.fit(X_train, y_train)
    selected_feat= X_train.columns[(sel.get_support())]
    
    new_train = pd.DataFrame().assign(case_id=train[case])
    new_test = pd.DataFrame().assign(case_id=test[case])
    new_val = pd.DataFrame().assign(case_id=val[case])
    
    for i in selected_feat:
        new_train[i]=train[i]
        new_test[i]=test[i]
        new_val[i]=val[i]
    
    print(len(new_train.columns))   
    print(len(new_test.columns))   
    print(len(new_val.columns))   
    
    new_train.to_csv(save_path + modality + "_train.csv", index=False)
    new_test.to_csv(save_path + modality + "_test.csv", index=False)
    new_val.to_csv(save_path + modality + "_val.csv", index=False)
