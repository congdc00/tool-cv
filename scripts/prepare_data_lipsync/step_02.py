import cv2
import os
import shutil
from core.face_detection import face_detection
from convert_background import convert_background
from datetime import datetime, timedelta
import math
from glob import glob
import time
from tqdm import tqdm
from loguru import logger
LOG_FFMPEG = "quiet"
TMP_PATH = "tmp/"

DATA_PATH = "./data/"
REMOVE_BG = False
SCALE_BB = 1.2 # Ty le crop vuot khoi boudding box
TB = 0.2 # Ty le nang frame len tren khuon mat
LOG_PATH = "./logs/"
# Ty le crop thanh mot frame co dinh
REC_SIZE = 0.8
NSMOOTH = 0.2 # cang thap chuyen dong cang muot
import argparse


def split_audio(video_path):
    os.system(f"ffmpeg -i {video_path} {TMP_PATH}output.wav")

def convert_frame(frame, bounding_box):

    padding_color = [0, 0, 0]
    t_pad, b_pad, l_pad, r_pad = 0,0,0,0
    
    h, w, _ = frame.shape

    if bounding_box[0][0] < 0:
        l_pad = -bounding_box[0][0]
    if bounding_box[0][1] < 0:
        t_pad = -bounding_box[0][1] 
    if bounding_box[1][0] > w:
        r_pad = bounding_box[1][0] - w 
    if bounding_box[1][1] > h:
        b_pad = bounding_box[1][1] - h

    bounding_box[0][0] += l_pad
    bounding_box[1][0] += l_pad 
    bounding_box[0][1] += t_pad
    bounding_box[1][1] += t_pad
    
    # print(f"l_pad {l_pad}; t_pad {t_pad}, b_pad {b_pad}, r_pad{r_pad}")
    
    return cv2.copyMakeBorder(frame, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT), bounding_box

def process_video(video_path, idx_start, folder_output_path):
    command = f"ffmpeg -loglevel quiet -i {video_path} -vn -acodec copy {TMP_PATH}audio.aac" 

    os.system(command)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    i = -1
    index_folder = 0
    is_face_pre = False
    list_time_start = []
    list_time_end = []
    is_start_flag= False
    x_center_old = 0 
    y_center_old = 0
    while True:
        i+=1
        
        ret, frame = cap.read()
        if not ret:
            break

        # face detection
        is_face, x_center, y_center,x_left, y_left, x_right, y_right= face_detection(frame)
        
        if x_center_old != 0 and y_center_old!=0:
            


            if int(round((x_center - x_center_old) * NSMOOTH, 0)) == 0:
                n_smooth = 0.7
            else:
                n_smooth = NSMOOTH
            # print(f"x_center {x_center}; x_center_old {x_center_old}; move {int(round((x_center - x_center_old) * n_smooth, 0))}")
            x_center = x_center_old + int(round((x_center - x_center_old) * n_smooth, 0))
            
            if int((y_center - y_center_old)*NSMOOTH) == 0:
                n_smooth = 0.7
            else:
                n_smooth = NSMOOTH
            y_center = y_center_old + int((y_center - y_center_old) * n_smooth)

        # nguong cat video 

        # Crop & Remove
        if is_face:
            
            bonus_x = int(((x_right-x_left)/2)*(1+SCALE_BB))
            bonus_y = int(((y_right-y_left)/2)*(1+SCALE_BB))
            img_size_cross = int(((x_left - x_right)**2 + (y_left-y_right)**2)**0.5 * SCALE_BB)
            padding = int(((y_right-y_left)/2)*TB)
            top_left =[x_center - bonus_x, y_center - bonus_y - padding]
            bottom_right = [x_center + bonus_x, y_center + bonus_y - padding]
            bb = [top_left, bottom_right]
            
            #print(f"old bb {bb}")
            #print(f"old frame {frame.shape}")
            frame, bb = convert_frame(frame, bb)
            #print(f"new bb {bb}")
            #print(f"new frame {frame.shape}")

            frame_face = frame[bb[0][1]:bb[1][1], bb[0][0] : bb[1][0]]
            if not is_start_flag:
                if i%fps !=0:
                    continue


                time_start = int(i/fps)  
                hours, minutes, seconds = time_start//3600, time_start//60, time_start-(time_start//60)*60 
                list_time_start.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}") 
                is_start_flag = True
                
                # print(f"start {list_time_start[-1]}")
                 
                index_folder += 1
                folder_frames = f"{TMP_PATH}frames_{index_folder:02d}/"
                os.makedirs(folder_frames, exist_ok = True)
                h_rec, w_rec, _= frame_face.shape 
                h_rec = int(h_rec*0.8)
                w_rec = int(h_rec*0.8)

            # print(f"i {i} x_center {x_center} x_center_old {x_center_old} y_center {y_center} y_center_old {y_center_old}")

            h, w, _= frame_face.shape
            # print(f"h {h} w {w}")
            centerpoint = h//2, w//2
            # print(f"frame_face {frame_face.shape}")

            # print(f"[{centerpoint[0] - h_rec//2}:{centerpoint[0] + h_rec//2}, {centerpoint[1] - w_rec//2}:{centerpoint[1]+w_rec//2}]")
            bb_2 = [[centerpoint[1] - w_rec//2, centerpoint[0] - h_rec//2], [centerpoint[1]+w_rec//2, centerpoint[0] + h_rec//2]]
            rec_frame, bb_3 = convert_frame(frame_face, bb_2)
            rec_frame = rec_frame[bb_3[0][1]: bb_3[1][1], bb_3[0][0] : bb_3[1][0]]
            
            
            # rec_frame = frame_face[centerpoint[0] - h_rec//2:centerpoint[0] + h_rec//2, centerpoint[1] - w_rec//2:centerpoint[1]+w_rec//2]
            if REMOVE_BG:
                rec_frame = convert_background(rec_frame)
            
            path_save =f"{folder_frames}{i:04d}.png"
            # print(f"path save {path_save}") 
            cv2.imwrite(f"{folder_frames}{i:04d}.png", rec_frame)

            x_center_old = x_center
            y_center_old = y_center
        else:
            if is_start_flag:
                time_end = math.floor(i/fps)
                hours, minutes, seconds = time_end//3600, time_end//60, time_end-(time_end//60)*60 
                list_time_end.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                is_start_flag = False
                
                # clear frame du thua
                i_end = int(time_end*fps)
                for idx in range(i_end, i):
                    path_rm =f"{folder_frames}{idx:04d}.png" 
                    # print(f"remove path {path_rm}")
                    os.remove(path_rm)
                
                x_center_old = 0 
                y_center_old = 0
                # print(f"end {list_time_end[-1]}")


    cap.release()

    #Check lan cuoi 
    if is_start_flag:
        time_end = math.floor(i/fps)
        hours, minutes, seconds = time_end//3600, time_end//60, time_end-(time_end//60)*60 
        list_time_end.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    z = 0
    # xoa het 
    list_result = []
    for i_start, i_end in zip(list_time_start, list_time_end):
        z+=1
        # qua ngan
        hours_s, minutes_s, seconds_s = i_start.split(":")
        hours_e, minutes_e, seconds_e = i_end.split(":")
        folder = f"{TMP_PATH}frames_{z:02d}/" 
        
        if hours_s == hours_e and minutes_s == minutes_e:
            ss = int(seconds_s)
            se = int(seconds_e)
            if se-ss < 2:
                shutil.rmtree(folder)
                continue

        basename = TMP_PATH + f"frames_{z:02d}.aac"
        command =f"ffmpeg -y -loglevel quiet -i {TMP_PATH}audio.aac -ss {i_start} -to {i_end} -c copy {basename}"               
        os.system(command)
        list_result.append([i_start, i_end, basename, folder])
    
    os.remove(f"{TMP_PATH}audio.aac") 
    # merge video 
    new_list_result = []
    for idx, result in enumerate(list_result):
        folder_source = result[-1]
        video_result = result[-1].split("/")[0] + "/" + result[-1].split("/")[1] + ".mp4"
        os.system(f"ffmpeg -loglevel quiet -framerate {fps} -pattern_type glob -i '{folder_source}*.png' -c:v libx264 -pix_fmt yuv420p {video_result}")
        audio_result = result[-2]
        os.system(f"ffmpeg -y -loglevel quiet -i {video_result} -i {audio_result} -c:v copy -c:a aac {folder_output_path}{idx_start:04d}_{idx:03d}.mp4")
        new_list_result.append([result[0], result[1], video_result])
    return new_list_result

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mô tả về chương trình.')
    parser.add_argument('--input_path', type=str, help='Mô tả tham số 1.')
    args = parser.parse_args()
    
    current_time = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    os.makedirs(LOG_PATH, exist_ok=True)
    log_path = LOG_PATH + f"{current_time}.txt" 
    tmp_path ="tmp/"
    
    if os.path.exists(TMP_PATH):
        shutil.rmtree(TMP_PATH)
    
    with open(log_path, 'a') as file:
        
        # lay cac videos
        # Kiem tra cac thu muc con 
        list_video = []
        list_folder = os.listdir(args.input_path)
        for folder_path in list_folder:
            input_path = args.input_path + folder_path + "/"
            
            list_video += glob(f"{input_path}*.mp4")
        if len(list_video)>0:
            logger.info(f"Load {len(list_video)} videos from {args.input_path}")
            output_path = DATA_PATH + os.path.basename(os.path.normpath(args.input_path)) + "/"
            os.makedirs(output_path, exist_ok=True)
        else:
            logger.error(f"No videos in path")
 
        for idx_start, video_path in tqdm(enumerate(list_video), desc="Processing items", total=len(list_video)):
            file.write("\n+++process\n")
            file.write(f"input: {video_path}\n")
            os.makedirs(TMP_PATH, exist_ok = True) 
            try:
                list_result = process_video(video_path, idx_start, output_path)
                file.write(f"status: OK\n")
                for result in list_result:
                    file.write(f"output: {result[-1]}, time: [{result[0]},{result[1]}]\n")
            except:
                file.write(f"status: False\n")
            shutil.rmtree(tmp_path)
        logger.success(f"Data save in {output_path}")
        
