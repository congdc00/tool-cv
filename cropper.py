from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import argparse
from loguru import logger
# Example
# python cropper.py -center_point () -size (<width>, <height>) -i <input_path> -o <output_path>  
TYPE_IMAGE = ["png", "jpg", "jpeg"]
TYPE_VIDEO = ["mp4"]
def parse_args():
    parser =  argparse.ArgumentParser(description="Run cropper")
    parser.add_argument("--center_point", "-c", default=("auto", "auto"), help="")
    parser.add_argument("--size", default=("auto", "auto"), help = "")
    parser.add_argument("--input_path", "-i", type=str, help = "")
    parser.add_argument("--output_path", "-o", type=str, help = "") 
    return parser.parse_args()

def load_data(input_path):
    basename = os.path.basename(input_path)
    if "." in basename:
        list_path = [input_path]
        if basename.split(".")[-1] in TYPE_VIDEO:
            return "videos", list_path
        elif basename.split(".")[-1] in TYPE_IMAGES:
            return "images", list_path
    else:
        for type_image in TYPE_IMAGE:
            list_img_path = glob.glob(input_path + f"/*.{type_image}")
            if len(list_img_path) > 0:
                return "images", list_img_path
        for type_video in TYPE_VIDEO:
            list_vid_path = glob.glob(input_path + f"/*.{type_video}")
            if len(list_vid_path) > 0:
                return "videos", list_vid_path
    return False

def get_wd(default_value, target_value):
    coordinate = []
    for i in range(2):
        if target_value[i] == "auto":
            coordinate.append(default_value[i]//2)
        else:
            coordinate.append(target_value[i])
    return coordinate

def crop_images(list_img_path, args):
    for idx, img_path in enumerate(tqdm(list_img_path, desc="Processing", unit="file")):
        image = Image.open(img_path)
        basename = os.path.basename(img_path).split(".")[0]
        basename = int(basename)
        
        if idx == 0:
            center_point = get_wd(image.size, args.center_point)
            size = get_wd(image.size, args.size)
 
        cropped_image = image.crop((center_point[0] - size[0], center_point[1] - size[1], \
                                    center_point[0] + size[0], center_point[1] + size[1]))
        cropped_image.save(f"{args.output_path}/{basename:04d}.png")
    return True

def crop_video():
    pass
if __name__ == "__main__":
    args = parse_args()
    type_data, list_path = load_data(args.input_path)
    if type_data == "videos":
        pass
        logger.success(f"Processd {len(list_path)} videos")
    elif type_data == "images":
        crop_images(list_path, args)
        logger.success(f"Processed {len(list_path)} images")

    else:
        logger.error(f"Type data not define")
