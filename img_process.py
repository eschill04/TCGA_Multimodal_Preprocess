import os
import slideio #MUST INSTALL FIRST
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
from PIL import Image

# get list of ids
id_df = pd.read_csv("../../../eschill4_multimodal_data/id_ttv_split_shuffled.csv")
ids = id_df["id"].tolist()
categories = id_df["cat"].tolist()

ORGANIZED_BY_CASE_PATH = "/users/eschill4/data/TCGA_Data/project_LUAD/data_by_cases/"
save_path = "../../../eschill4_multimodal_data/image_experimental/"
# Can change the save path to something compatible with your set-up
# Wherever you make new directory, make sure to have image_train, image_test, and image_val folders
# inside!!!
 

#-- goes through list of case_ids
def get_FFPE_images(case):
    img_files = os.listdir(os.path.join(ORGANIZED_BY_CASE_PATH, case, "images"))
    for f in img_files:
        if (f.split('.')[0][-3:-1] == 'DX'):
            return os.path.join(ORGANIZED_BY_CASE_PATH, case, 'images', f)
    print("No DX found for case",case)
    return None


valid_case_paths = {}
j = 0
for case in ids:
    n = get_FFPE_images(case)
    if n is not None:
        valid_case_paths[case] = n
        j+=1
print(f"{j} cases out of {len(ids)} have valid images")

orig_dims = []

for (case, img_path) in valid_case_paths.items():

    #-- indexes into images folder for that case
    
    slide = slideio.open_slide(img_path,'SVS')
    scene = slide.get_scene(0)
    
    dims = (scene.rect[2], scene.rect[3])
    orig_dims.append(dims)
    
aspect_ratio = [x/y for x, y in orig_dims]

med_aspect_ratio = round(np.median(aspect_ratio), 4)
print(f"Median aspect ratio: {med_aspect_ratio}")

h = 300
w = round(med_aspect_ratio * h)
print(f"Width: {w}, Height: {h}")

for (case, img_path) in valid_case_paths.items():

    slide = slideio.open_slide(img_path,'SVS')
    scene = slide.get_scene(0)
    image = scene.read_block(size=(0,h))
    orig_width = image.shape[1]
    
    '''
    Old padding script here:
    final_img = np.empty([h, w, 3])
    
    if height > h:
        middle = height//2
        diff = h//2 + 1
        final_img = image[middle-diff:middle+diff,:,:]
        
    if height < h:
        edge = (h - height)//2
        final_img = np.pad(image, ((edge + 1, edge + 1), (0, 0), (0, 0)), constant_values=(255,))

    final_img = (final_img[:h,:,:]).clip(0, 255)
    '''
        
    
    print("orig dims:", image.shape)
    new_image = Image.fromarray(image)
    if(h > orig_width):
        new_image = new_image.transpose(Image.ROTATE_90)
        
    resized_image = new_image.resize((w, h))
    print("final dims:", resized_image.size)
    
    #-- saves the nparray to a jpeg file based on category
    
    print(case, "successful")
    
    cat = categories[ids.index(case)]
    
    if cat == 0:
        resized_image.save(save_path + "image_train/" + case + '.jpg')
    elif cat == 1:
        resized_image.save(save_path + "image_test/" + case + '.jpg')
    else:
        resized_image.save(save_path + "image_val/" + case + '.jpg')





