import os
from glob import glob
import json
import csv
NAME_DATASET = "./data/data_lipsync"

if __name__ == "__main__":
    list_root = glob(f"{NAME_DATASET}/*")
    list_word = {}
    
    for root_path in list_root:
        r_path = f"{root_path}/step_05"
        
        list_id = glob(f"{r_path}/*") 
        for id_path in list_id:
            videos_path = id_path + "/videos"
            list_video = glob(f"{videos_path}/*")
            for video_path in list_video:
                list_info = glob(f"{video_path}/*.json")
                for info_path in list_info:
                    with open(info_path, 'r', encoding='utf-8') as file:
                        data = json.load(file) 
                        text = data["metadata"]["text"].lower()
                        text = text.replace("...", "")
                        text = text.replace(".", "")
                        text = text.replace(",", "")
                        text = text.replace("?", "")
                    words = text.split(" ")
                    for word in words:
                        if word in list_word:
                            count = list_word[word]
                            count += 1
                            list_word[word] = count
                        else:
                            list_word[word] = 1
    
    with open("test.csv", 'w', newline='') as csv_file:
        fieldnames = ['word', 'num']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for key, value in list_word.items():
            content = {"word": key, "num": value}
            csv_writer.writerow(content) 
