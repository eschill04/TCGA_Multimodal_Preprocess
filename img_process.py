import os
import slideio 
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
from PIL import Image


ID_PATH = "../../../eschill4_multimodal_data/id_ttv_split_shuffled.csv"
ORGANIZED_BY_CASE_PATH = "/users/eschill4/data/TCGA_Data/project_LUAD/data_by_cases/"
SAVE_PATH = "../../../eschill4_multimodal_data/image_experimental/"

id_df = pd.read_csv(ID_PATH)
ids = id_df["id"].tolist()
categories = id_df["cat"].tolist()

'''
Given a Case ID, return the path to the correct (DX) .svs image for that Case ID. 
'''
def get_FFPE_images(case):
    img_files = os.listdir(os.path.join(ORGANIZED_BY_CASE_PATH, case, "images"))
    for f in img_files:
        if (f.split('.')[0][-3:-1] == 'DX'):
            return os.path.join(ORGANIZED_BY_CASE_PATH, case, 'images', f)
    print("No DX found for case",case)
    return None

'''
Populate a dictionary of Case ID's and their image paths.
'''
valid_case_paths = {}
j = 0
for case in ids:
    n = get_FFPE_images(case)
    if n is not None:
        valid_case_paths[case] = n
        j+=1
print(f"{j} cases out of {len(ids)} have valid images")

'''
Populate a list of image dimensions to calculate the median aspect ratio.
'''
orig_dims = []
for (case, img_path) in valid_case_paths.items():
    
    slide = slideio.open_slide(img_path,'SVS')
    scene = slide.get_scene(0)
    
    dims = (scene.rect[2], scene.rect[3])
    orig_dims.append(dims)
    
aspect_ratio = [x/y for x, y in orig_dims]

med_aspect_ratio = round(np.median(aspect_ratio), 4)
print(f"Median aspect ratio: {med_aspect_ratio}")


'''
Transpose all vertical images to avoid excessive distortion.
Resize all images to new dimensions based on median aspect ratio.
Finally, save image as .jpg in either image_train, image_test, or image_val folder.
'''
h = 300
w = round(med_aspect_ratio * h)
print(f"New Width: {w}, New Height: {h}")

for (case, img_path) in valid_case_paths.items():

    slide = slideio.open_slide(img_path,'SVS')
    scene = slide.get_scene(0)
    image = scene.read_block(size=(0,h))
    orig_width = image.shape[1]
    
    new_image = Image.fromarray(image)
    if(h > orig_width):
        new_image = new_image.transpose(Image.ROTATE_90)
        
    resized_image = new_image.resize((w, h))
        
    print(case, "successful")
    
    cat = categories[ids.index(case)]
    
    if cat == 0:
        resized_image.save(SAVE_PATH + "image_train/" + case + '.jpg')
    elif cat == 1:
        resized_image.save(SAVE_PATH + "image_test/" + case + '.jpg')
    else:
        resized_image.save(SAVE_PATH + "image_val/" + case + '.jpg')





