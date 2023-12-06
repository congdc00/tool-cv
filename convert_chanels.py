import cv2

# Đọc ảnh 3 kênh màu
image = cv2.imread("./data/input.png")

# Chuyển ảnh sang 4 kênh màu
image_rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

# Lưu ảnh 4 kênh màu
cv2.imwrite("./data/output.png", image_rgba)

