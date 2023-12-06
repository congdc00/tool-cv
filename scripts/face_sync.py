import cv2
import os
import shutil
from core.face_detection import face_detection
LOG_FFMPEG = "quiet"
TMP_PATH = "tmp/"

def split_audio(video_path):
    os.system(f"ffmpeg -i {video_path} {TMP_PATH}output.wav")

def convert_lines(lines):
    new_lines = []
    for i in range(1, len(lines)):
        if lines[i] > lines[i-1]:
            pass 

def get_points(left_index, points):
    lines = []
    new_lines = []
    for i in range(1, len(left_index)):
        first_point_i = left_index[i-1]
        second_point_i = left_index[i]

        first_point = points[first_point_i]
        second_point = points[second_point_i]

        num_split = abs(second_point[1] - first_point[1]) + 1 
        # xac dinh dau cho stride 
        if int(second_point[0]-first_point[0]) != 0:
            type_stride = (second_point[0] - first_point[0])/abs(second_point[0] - first_point[0])
            x_stride = type_stride*abs(first_point[0] - second_point[0])/num_split
        else:
            x_stride = 0
        y_stride = 1
        
        x_start, y_start = first_point
        for j in range(abs(first_point[1] - second_point[1])):
            x_start += x_stride

            # if len(lines) == 50:
            lines.append((round(x_start), y_start))

            y_start += y_stride
    # lines = convert_lines(lines)
    lines.append((round(x_start), y_start))
    return lines

def process_video(input_path, target_path):
    cap1 = cv2.VideoCapture(target_path)
    cap2 = cv2.VideoCapture(input_path)
    fps = cap1.get(cv2.CAP_PROP_FPS)
    
    left_index = [10, 109, 67, 103, 54, 21, 162, 127, 234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 152]
    right_index = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152]

    i = 0
    index_folder = 0
    is_face_pre = False
    while True:
        ret, frame = cap1.read()
        _, root_frame = cap2.read()
        if not ret:
            break
        points = face_detection(frame)
                
        if i == 0:
            folder_frames = f"{TMP_PATH}frames_{index_folder:02d}/"
            os.makedirs(folder_frames, exist_ok = True)
        left_points = get_points(left_index, points)              
        right_points = get_points(right_index, points)
        '''
        for p_r, p_l in zip(right_points,left_points):
            cv2.circle(frame, p_r, 0, (0, 0, 255) , thickness=0)
            cv2.circle(frame, p_l, 0, (0, 0, 255) , thickness=0)
            print(f"left {p_l} right {p_r}")
        cv2.imwrite(f"{folder_frames}{i:04d}.png", frame)'''

        h, w, _ = frame.shape
        line_check = 0
        PAD = 10
        padding = 0
        for k in range(h):
            check_continue=True
            for j in range(w):
                if check_continue and k >= right_points[0][1] and k<=right_points[-1][1] + PAD:
                    if line_check < len(left_points):
                        if j>=left_points[line_check][0] and j<=right_points[line_check][0]:
                            if j==right_points[line_check][0]:
                                if line_check == 3*line_check//4 and padding <PAD:
                                    padding += 1
                                else:
                                    line_check+=1
                                check_continue = False
                                
                            root_frame[k][j]=frame[k][j]
        cv2.imwrite(f"{folder_frames}{i:04d}.png", root_frame)
        i+=1
    cap1.release()

if __name__ == "__main__":
    
    # prepare workspace
    tmp_path ="tmp/"
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    os.mkdir(tmp_path)
    
    input_video = "./data/source_01.mp4"
    target_video = "./data/target_01.mp4"
    process_video(input_video, target_video)
