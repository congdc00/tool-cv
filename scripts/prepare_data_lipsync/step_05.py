import os
from glob import glob
import shutil
from core.speech2text import S2T_Model
from tqdm import tqdm
import json
ROOT_PATH = "/home/congdc/hdd/tool-cv"
NAME_DATASET = "./data/data_lipsync/chunk_02/"
INPUT_PATH = f"{NAME_DATASET}step_04/"
OUTPUT_PATH = f"{NAME_DATASET}step_05/"
TMP_PATH = f"{ROOT_PATH}/tmp/"

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        shutil.copytree(INPUT_PATH, OUTPUT_PATH)
    list_input = glob(f"{OUTPUT_PATH}/*")
    for root_path in list_input:
        input_path = root_path + "/" + "videos"
        list_video = glob(f"{input_path}/*")
        for v_path in tqdm(list_video):
            videos_path = glob(f"{v_path}/*.mp4")
            for video_path in videos_path:
                info_path = video_path.replace(".mp4", ".json")
                if os.path.exists(TMP_PATH):
                    shutil.rmtree(TMP_PATH)
                os.mkdir(TMP_PATH)
                command = f"ffmpeg -loglevel quiet -i {video_path} -vn -acodec copy {TMP_PATH}audio.aac"
                os.system(command)
                text = S2T_Model.convert(f"{TMP_PATH}audio.aac")
                with open(info_path, "w",encoding='utf-8' ) as f:
                    data = {
                            "metadata": {
                                "text": text
                            }}
                    json.dump(data, f,ensure_ascii=False , indent=4)
