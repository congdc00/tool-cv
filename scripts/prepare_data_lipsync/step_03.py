import os 
from glob import glob 
DATA_PATH = "./data/data_lipsync/chunk_02"
STEP = 3
import shutil
import json

template_info = {
        "gender": "",
        "language": {
            "nation":"vietnamese",
            "area": ""
            }
        }

if __name__ == "__main__":
    ns_path = DATA_PATH + f"/step_{STEP:02d}"
    
    data_path = ns_path + "/*"
    list_group = glob(data_path)
    
    for group in list_group:
        folder_name = os.path.basename(group)
        tmp_path = group.replace(folder_name, "videos")

        os.makedirs(tmp_path)
        list_vid = glob(f"{group}/*")
        for i, vid_path in enumerate(list_vid):
            name_vid = f"{i:05d}" + "." + vid_path.split(".")[-1]
            target_path = tmp_path + "/" + name_vid
            shutil.move(vid_path, target_path)
        
        shutil.move(tmp_path, group)
    
        json_path = group + "/info.json"
        with open(json_path, 'w') as f:
            json.dump(template_info, f, indent=4)

    

