from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import shutil

BASE = "name"
START_I = 0

input_path = "./data/images/"
output_path = "./data/output/"
os.makedirs(output_path, exist_ok=True)
list_img_path = glob.glob(input_path + "/*")

if BASE == "random":
    i = 0
    for source_path in tqdm(list_img_path, desc="Processing", unit="file"):
        i += 1
        base_name = os.path.basename(source_path).split(".")[0]
        base_name = i
        base_name = "{:04d}".format(base_name)
        destination_path = f"{output_path}/{base_name}.png"
        shutil.copy(source_path, destination_path)
elif BASE == "name":
    i=0
    for source_path in tqdm(list_img_path, desc="Processing", unit="file"):
        base_name = os.path.basename(source_path).split(".")[0]
        if "-" in base_name:
            number = base_name.split("-")[1]
        elif "_" in base_name:
            number = base_name.split("_")[0]
        else:
            number = base_name
        base_name = int(number) - START_I
        #base_name = "{:03d}".format(base_name)
        destination_path = f"{output_path}/{base_name}.jpg"
        shutil.copy(source_path, destination_path)
        i+=1
