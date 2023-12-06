import os
from glob import glob
import shutil
from core.speech2text import S2T_Model
from tqdm import tqdm
import json

NAME_DATASET = "data_lipsync/chunk_01/"
INPUT_PATH = f"{NAME_DATASET}step_04/"
OUTPUT_PATH = f"{NAME_DATASET}step_05/"
TMP_PATH = "tmp/"

if __name__ == "__main__":
    folder_path = f"{INPUT_PATH}*.json"
    list_input = glob(folder_path)
    for info_path in tqdm(list_input):
        with open(info_path, "r") as f:
            data = json.load(f)
         
        vid_path = info_path.replace("json", "mp4")
        # create workspace
        if os.path.exists(TMP_PATH):
            shutil.rmtree(TMP_PATH)
        os.mkdir(TMP_PATH)
        
        command = f"ffmpeg -loglevel quiet -i {vid_path} -vn -acodec copy {TMP_PATH}audio.aac"
        os.system(command)

        text = S2T_Model.convert(f"{TMP_PATH}audio.aac")
        
        data["metadata"]["text"] = text       
        
        #save data
        target_path = info_path.replace(INPUT_PATH, OUTPUT_PATH)
        with open(target_path, "w") as f:
            json.dump(data, f, ensure_ascii=False)
        target_path = vid_path.replace(INPUT_PATH, OUTPUT_PATH)
        shutil.copy(vid_path, target_path)
