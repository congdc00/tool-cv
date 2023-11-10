from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import shutil

BASE = "name"

input_path = "./data/output_tmp1"
output_path = "./data/output_tmp2"

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
    for source_path in tqdm(list_img_path, desc="Processing", unit="file"):
        base_name = os.path.basename(source_path).split(".")[0]
        if "-" in base_name:
            number = base_name.split("-")[1]
        elif "_" in base_name:
            number = base_name.split("_")[0]
        else:
            number = base_name
        base_name = int(number)
        base_name = "{:04d}".format(base_name)
        destination_path = f"{output_path}/{base_name}.png"
        shutil.copy(source_path, destination_path)
