import torch
import onnxruntime as rt
from rembg import remove,new_session 
from PIL import Image
import glob
import os
from tqdm import tqdm
import rawkit 
input_path = "./data/input_tmp"
output_path = "./data/output_tmp"
type_images = "png"
list_img_path = glob.glob(input_path + f"/*.{type_images}")

class Remover():
    
    session = None
    
    @staticmethod
    def __init_session():
        Remover.session = new_session("u2net_human_seg")
    
    @staticmethod
    def get_session():
        if Remover.session == None:
            Remover.__init_session()

        return Remover.session

def convert_background(image_root, background_target=None):
    # for img_path in tqdm(list_img_path, desc="Processing", unit="file"):
    #     if type_images == "CR2":
    #         with rawkit.CR2File(img_path) as cr2_file:
    #             image_data = cr2_file.get_image_data()
    #             img_input = np.frombuffer(image_data, dtype=np.uint8)
    #     else:
    #         img_input = Image.open(img_path)
    session = Remover.get_session()
    img_none_bg = remove(image_root, session = session)

    return img_none_bg