import os
from glob import glob
import shutil
from core.speech2text import S2T_Model
from tqdm import tqdm
import json
from convert_background import convert_background

NAME_DATASET = "data_lipsync/chunk_01/"
INPUT_PATH = f"{NAME_DATASET}step_02/"
OUTPUT_PATH = f"{NAME_DATASET}step_03/"
TMP_PATH = "tmp/"

if __name__ == "__main__":
    logger.info(f"Process {NAME_DATASET} step 3")

    folder_path = f"{INPUT_PATH}*.json"
    list_input = glob(folder_path)
    for info_path in tqdm(list_input):

        
        vid_path = info_path.replace("json", "mp4")
        fps = cap.get(cv2.CAP_PROP_FPS)
 
        # create workspace
        if os.path.exists(TMP_PATH):
            shutil.rmtree(TMP_PATH)
        os.mkdir(TMP_PATH)
        
        command = f"ffmpeg -loglevel quiet -i {vid_path} -vn -acodec copy {TMP_PATH}audio.aac"
        os.system(command)
        
        cap = cv2.VideoCapture(video_path)
        i = 0
        while True:
            i+=1

            name_video = os.path.basename(video_path)
            
            ret, frame = cap.read()
            if not ret:
                break

            frame = convert_background(frame)
            cv2.imwrite(f"{TMP_PATH}{i:04d}.png", frame)
        
        # merge video
        command = f"ffmpeg -loglevel quiet -framerate {fps} -pattern_type glob -i '{TMP_PATH}*.png' -c:v libx264 -pix_fmt yuv420p {TMP_PATH}{name_video}"
        os.system(command)

        # merge audio
        os.system(f"ffmpeg -y -loglevel quiet -i {TMP_PATH}{name_video} -i {TMP_PATH}audio.aac -c:v copy -c:a aac {OUTPUT_PATH}{name_vide}")
 
        #save data
        target_path = info_path.replace(INPUT_PATH, OUTPUT_PATH)
        shutil.copy(info_path, target_path)
    
        break
