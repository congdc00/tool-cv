from PIL import Image
import os

def combine_images(input_folder_top, input_folder_bottom, output_folder):
    # Lấy danh sách các tệp ảnh từ thư mục nửa trên
    top_images = os.listdir(input_folder_top)
    
    # Lặp qua từng tệp ảnh
    for image_name in top_images:
        # Tạo đường dẫn đầy đủ cho nửa trên và nửa dưới
        top_path = os.path.join(input_folder_top, image_name)
        bottom_path = os.path.join(input_folder_bottom, image_name)
        
        # Mở ảnh từ đường dẫn
        top_image = Image.open(top_path)
        bottom_image = Image.open(bottom_path)
        
        # Lấy kích thước của ảnh nửa trên
        width, height = top_image.size
        
        # Lấy nửa trên của ảnh và nửa dưới của ảnh
        top_half = top_image.crop((0, 0, width, height // 2))
        bottom_half = bottom_image.crop((0, height // 2, width, height))
        
        # Tạo ảnh mới bằng cách kết hợp nửa trên và nửa dưới
        new_image = Image.new("RGB", (width, height), (255, 255, 255))  # Ảnh mới có nền trắng
        new_image.paste(top_half, (0, 0))
        new_image.paste(bottom_half, (0, height // 2))
        
        # Lưu ảnh kết quả vào thư mục đầu ra
        output_path = os.path.join(output_folder, image_name)
        new_image.save(output_path)

if __name__ == "__main__":
    input_folder_top = "./data/nua_tren/"
    input_folder_bottom = "./data/nua_duoi/"
    output_folder = "./data/output/"
    
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Gọi hàm để kết hợp ảnh
    combine_images(input_folder_top, input_folder_bottom, output_folder)

