import glob
import shutil
import os

# Đường dẫn đến thư mục chứa các tệp ảnh PNG
source_folder = '/home/hgmedia/Project/tool-cv/data/best_result'

# Đường dẫn đến thư mục đích để sao chép tệp ảnh
destination_folder = '/home/hgmedia/Project/tool-cv/data/output_best_result'

# Sử dụng glob để lấy danh sách các tệp ảnh PNG trong thư mục nguồn
png_files = glob.glob(os.path.join(source_folder, '*.png'))

# Lặp qua danh sách các tệp ảnh PNG và sao chép chúng vào thư mục đích
i = 0
count=0
for png_file in png_files:
    i+=1
    if i%6==0:
        # Đường dẫn đến tệp trong thư mục đích
        destination_file = os.path.join(destination_folder, os.path.basename(png_file))
        # Sao chép tệp ảnh từ thư mục nguồn sang thư mục đích
        shutil.copy(png_file, destination_file)
        count+=1

print(f'{count} tệp ảnh PNG đã được sao chép vào {destination_folder}')
