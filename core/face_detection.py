import cv2
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
from loguru import logger 

class FaceDetect():
    face_mesh = None
    
    @staticmethod
    def init_face_mesh_model():
        logger.info("init face detectection")
        FaceDetect.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
    
    @staticmethod
    def get_face_mesh_model():
        if FaceDetect.face_mesh == None:
            FaceDetect.init_face_mesh_model()
        return FaceDetect.face_mesh

def round_num(value):
    return (value//2)*2


def face_detection(image_input, mode="one_detect"):
    image_rows, image_cols, _ = image_input.shape
    face_mesh = FaceDetect.get_face_mesh_model()
    results = face_mesh.process(cv2.cvtColor(image_input , cv2.COLOR_BGR2RGB))
    try:
        num_face = len(results.multi_face_landmarks)
        list_face = []
        for i_face in range(num_face):
            list_face.append(results.multi_face_landmarks[i_face].landmark)

    except:
        return False, _, _, _, _, _, _
    
        
    
    best_rec_face = 0

    for ls_single_face in list_face:
        points_tmp = []
        x_left_tmp = 9999
        y_left_tmp = 9999
        x_right_tmp = 0 
        y_right_tmp = 0 
        list_x_tmp = [] 
        list_y_tmp = []

        for i, idx in enumerate(ls_single_face):
            cord = _normalized_to_pixel_coordinates(idx.x,idx.y,image_cols,image_rows)
            #cap nhap bounding box
            x_left_tmp = min(x_left_tmp, cord[0])
            y_left_tmp = min(y_left_tmp, cord[1])
            x_right_tmp = max(x_right_tmp, cord[0])
            y_right_tmp = max(y_right_tmp, cord[1])

            # if i == 4:
                # x_center = cord[0]
                # y_center = cord[0]
            list_x_tmp.append(cord[0])
            list_y_tmp.append(cord[1])

            points_tmp.append(cord)
    
        # update main_face
        if abs(x_left_tmp - x_right_tmp)*abs(y_left_tmp-y_right_tmp) > best_rec_face:

            x_left = x_left_tmp
            y_left = y_left_tmp
            x_right = x_right_tmp
            y_right = y_right_tmp
            list_x = list_x_tmp
            list_y = list_y_tmp
            points = points_tmp

            best_rec_face = abs(x_left_tmp - x_right_tmp)*abs(y_left_tmp-y_right_tmp)  

    ## for swapface

    x_center = int(sum(list_x)/len(list_x))
    y_center = int(sum(list_y)/len(list_y))
      
    return True, x_center, y_center, x_left, y_left, x_right, y_right  

if __name__ == "__main__":
    frame = cv2.imread("0125.png")
    is_face, points, bounding_box = face_detection(frame)
    print(is_face) 
    # cv2.putText(image_input, '.', top_left,cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)
    # cv2.putText(image_input, '.', bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)
    # 
    # cv2.imwrite("test.png", image_input)

