import torch
import onnxruntime as rt
from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import rawkit 
input_path = "./data/input_tmp"
output_path = "./data/output_tmp"
type_images = "png"
list_img_path = glob.glob(input_path + f"/*.{type_images}")

for img_path in tqdm(list_img_path, desc="Processing", unit="file"):
    if type_images == "CR2":
    	with rawkit.CR2File(img_path) as cr2_file:
	        image_data = cr2_file.get_image_data()
	        img_input = np.frombuffer(image_data, dtype=np.uint8)
    else:
    	img_input = Image.open(img_path)
    	
    img_name = os.path.basename(img_path)
    img_none_bg = remove(img_input)
    img_none_bg.save(f"{output_path}/{img_name}")
