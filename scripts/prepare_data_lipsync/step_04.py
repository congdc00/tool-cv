from glob import glob
import ffmpeg
import os
import shutil
from tqdm import tqdm
DATA_PATH = "data/data_lipsync/chunk_02/step_04"
SAVE_PATH = "data/data_lipsync/chunk_02/step_04_tmp"
def get_durration(local_file_path):
    duration = ffmpeg.probe(local_file_path,loglevel="quiet" )["format"]["duration"]
    return duration
def split_time(duration):
    start_second = 0 
    end_second = int(float(duration))
    list_duration = []
    while end_second - start_second >= 3:
        s_second = start_second
        e_second = start_second + 3
        list_duration.append([s_second, e_second])
        start_second = e_second
    if end_second - start_second > 0:
        if len(list_duration) > 0:
            list_duration.pop()
        list_duration.append([start_second, end_second])
    return list_duration

if __name__ == "__main__":
    list_path = glob(f"{DATA_PATH}/*")
    os.makedirs(SAVE_PATH, exist_ok = True)

    for source_path in list_path:
        video_path = f"{source_path}/videos/"
        save_path = SAVE_PATH + "/" + os.path.basename(source_path)
        videos_path = save_path + "/videos"
        os.makedirs(save_path, exist_ok = True)
        os.makedirs(videos_path, exist_ok = True)
        list_video = glob(f"{video_path}/*")
        shutil.copy(f"{source_path}/info.json", f"{save_path}/")
        for video in tqdm(list_video):
            
            duration = get_durration(video)
            list_time = split_time(duration)
            name_sub_video = os.path.basename(video).split(".")[0]
            os.makedirs(f"{videos_path}/{name_sub_video}", exist_ok=True)
            for i, time_s in enumerate(list_time):
                s_time = time_s[0]
                e_time = time_s[1]
                
                name_video = f"{i:03d}.mp4"
                output_path = f"{videos_path}/{name_sub_video}/{name_video}"
                if not os.path.exists(output_path):
                    ffmpeg.input(video, ss=s_time, to=e_time,loglevel="quiet" ).output(output_path).run()
