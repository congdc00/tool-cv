import rawpy
import imageio
from PIL import Image
from glob import glob
from tqdm import tqdm
import os

# Đường dẫn đến p .CR2
input_path = "./data/CongDataset/"
output_path = "./data/output/"

list_file = glob(f"{input_path}/*")

for file in tqdm(list_file):
    basename = os.path.basename(file).split(".")[0]
    des_path = output_path + basename + ".png"

    with rawpy.imread(file) as raw:
        rgb = raw.postprocess()
        imageio.imsave(des_path, rgb)
