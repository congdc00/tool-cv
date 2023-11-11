from rembg import remove
from PIL import Image
import glob
import os
from tqdm import tqdm
import argparse
from loguru import logger
import cv2

import ffmpeg
# Example
# python cropper.py -center_point () -size (<width>, <height>) -i <input_path> -o <output_path>  
TYPE_IMAGE = ["png", "jpg", "jpeg"]
TYPE_VIDEO = ["mp4"]
LOG_FFMPEG = "quiet"
def parse_args():
    parser =  argparse.ArgumentParser(description="Run cropper")
    parser.add_argument("--center_point", "-c", default=["center_point", "center_point"], help="")
    parser.add_argument("--size", "-s", default=["center_point", "center_point"], help = "")
    parser.add_argument("--input_path", "-i", type=str, help = "")
    parser.add_argument("--output_path", "-o", default="./data/cropped_tmp/", type=str, help = "") 
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
    key_center_point = "center_point"
    if type(target_value) == str:
        x, y = target_value.replace("[", "").replace("]", "").split(",")
        target_value = []
        for i, value in enumerate([x,y]): 
            if key_center_point in value:
                # phan xu ly cho 
                value = value.replace(key_center_point, "")
                if value == "":
                    value = "0"
                root_point = default_value[i]//2
            else:
                root_point = 0
            value = root_point + int(value)
            target_value.append(value) 
    return target_value

def crop_images(list_img_path, args):
    for idx, img_path in enumerate(tqdm(list_img_path, desc="Processing", unit="file")):
        image = Image.open(img_path)
        basename = os.path.basename(img_path).split(".")[0]
        basename = int(basename)
        
        if idx == 0:
            center_point = get_wd(image.size, args.center_point)
            size = get_wd(image.size, args.size)
 
        cropped_image = image.crop((center_point[0] - size[0]//2, center_point[1] - size[1]//2, \
                                    center_point[0] + size[0]//2, center_point[1] + size[1]//2))
        cropped_image.save(f"{args.output_path}/{basename:04d}.png")
    return True

def crop_videos(list_video_path, args):
    for idx, vid_path in enumerate(tqdm(list_video_path, desc="Processing", unit="file")):
        basename = os.path.basename(vid_path)

        probe = ffmpeg.probe(vid_path)
        video = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        vid_size = [int(video['width']), int(video['height'])]
        if idx == 0:
            center_point = get_wd(vid_size, args.center_point)
            size = get_wd(vid_size, args.size)
            logger.info(f"INFO center_point [{center_point[0]},{center_point[1]}] size [{size[0]},{size[1]}]")
        video = ffmpeg.input(vid_path)
        images = video.video
        audio = video.audio
        
        images = images.filter('crop',\
                        size[0], size[1],\
                        center_point[0] - size[0]//2,center_point[1] - size[1]//2)
        output_path = args.output_path + "/" + basename
        ffmpeg.output(images, audio, output_path, acodec='libvorbis' ,vcodec='libx264', crf=22, loglevel=LOG_FFMPEG).overwrite_output().run()

if __name__ == "__main__":
    args = parse_args()
    
    if os.path.exists(args.output_path):
        logger.warning(f"Output path is exists")
        args.output_path += "_2" 
    os.makedirs(args.output_path, exist_ok=True)

    type_data, list_path = load_data(args.input_path)
    if type_data == "videos":
        logger.info("Mode: Videos")
        crop_videos(list_path, args)
        logger.success(f"Processd {len(list_path)} videos")
    elif type_data == "images":
        logger.info("Mode: Videos")
        crop_images(list_path, args)
        logger.success(f"Processed {len(list_path)} images")

    else:
        logger.error(f"Type data not define")
