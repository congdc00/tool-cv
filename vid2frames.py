from glob import glob
import os
import shutil
from tqdm import tqdm

DATA_PATH = "./data/AIClip/"
OUTPUT_PATH = "./data/AIClip/frames/"
if __name__ == "__main__":
    list_video = glob(f"{DATA_PATH}/*.mp4")

    with tqdm(total=len(list_video)) as pbar:
        for vid_path in list_video:
            new_vid_path = vid_path.replace(" ", "_")
            new_vid_path = new_vid_path.replace("(", "")
            new_vid_path = new_vid_path.replace(")", "")
            os.rename(vid_path, new_vid_path)

            name_video = os.path.basename(new_vid_path).split(".")[0]
            print(new_vid_path)
            command = f"ffmpeg -i {new_vid_path} -r 1 {OUTPUT_PATH}/{name_video}_%02d.png -loglevel error"
            os.system(command)
            pbar.update(1)
