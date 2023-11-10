from PIL import Image, ImageEnhance
import os
import random

# Đường dẫn tới thư mục chứa ảnh gốc
input_directory = './data/nerf_synthetic/ship/images'
# Đường dẫn tới thư mục lưu ảnh sau khi tăng độ sáng
output_directory = './data/nerf_synthetic/ship/images'

# Lấy danh sách các tệp tin .png trong thư mục đầu vào
input_images = [f for f in os.listdir(input_directory) if f.endswith('.png')]

# Lặp qua từng tệp tin ảnh
for image_file in input_images:
    # Đường dẫn đầy đủ của tệp tin ảnh đầu vào
    input_path = os.path.join(input_directory, image_file)
    # Mở ảnh sử dụng PIL
    image = Image.open(input_path)
    
    # Tăng độ sáng ngẫu nhiên
    brightness_factor = random.uniform(-0.7, 0.7)
    # Tăng độ sáng của ảnh
    brightened_image = ImageEnhance.Brightness(image).enhance(1 + brightness_factor)
    # Đường dẫn đầy đủ của tệp tin ảnh đầu ra
    output_path = os.path.join(output_directory, image_file)
    # Lưu ảnh tăng độ sáng xuống thư mục đầu ra
    brightened_image.save(output_path)

print("Đã xử lý xong tất cả các ảnh.")
