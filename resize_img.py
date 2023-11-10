from PIL import Image
import glob
import os
from tqdm import tqdm

# Config
width, height = 90, 120
input_path = "./data/heygen_plus/"
output_path = "./data/heygen_90x120/"

list_img_path = glob.glob(input_path + "/*.png")

for img_path in tqdm(list_img_path, desc="Processing", unit="file"):
    image = Image.open(img_path)
    img_name = os.path.basename(img_path)

    # Resize ảnh
    resized_image = image.resize((width, height))

    resized_image.save(f"{output_path}/{img_name}")

