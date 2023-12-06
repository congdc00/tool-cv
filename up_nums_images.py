from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import shutil
import argparse 

def parse_args():
    parser = argparse.ArgumentParser(description="")

input_path = "./data/nua_duoi"

list_img_path = glob.glob(input_path + "/*")
total_images = len(list_img_path)
for source_path in tqdm(list_img_path, desc="Processing", unit="file"):
    base_name = os.path.basename(source_path).split(".")[0]
    try:
    	number = base_name.split("-")[1]
    except:
    	number = base_name
    	
    base_name = - int(number) + 2*total_images + 1
    base_name = "{:04d}".format(base_name)
    destination_path = f"{input_path}/{base_name}.png"
    shutil.copy(source_path, destination_path)
