from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm

# Config
new_width, new_height = 1280, 1280
input_path = "./data/output_aiclip/"
output_path = "./data/output_aiclip_02"

list_img_path = glob.glob(input_path + "/*.png")
for img_path in tqdm(list_img_path, desc="Processing"):
    img = Image.open(img_path)
    width, height = img.size

    output = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    output.paste(img, (280, 0))

    img_name = os.path.basename(img_path)

    output.save(f"{output_path}/{img_name}")
