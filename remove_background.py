from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm

input_path = './data/input'
output_path = './data/output'

list_img_path = glob.glob(input_path + '/*.png')

for img_path in tqdm(list_img_path, desc='Processing', unit='file'):
    img_input = Image.open(img_path)
    img_name = os.path.basename(img_path)
    img_none_bg = remove(img_input)
    img_none_bg.save(f"{output_path}/{img_name}")