import os
from PIL import Image, ExifTags
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# 读取图像并解析元信息
image_path = 'IMG_4463.JPG'  # 图片路径
image = Image.open(image_path)
exif_data = image._getexif()

# 打印图像的元信息
if exif_data:
    for tag, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag, tag)
        print(f"{tag_name}: {value}")
else:
    print("没有元信息")

# 将图像转换为numpy数组
image_array = np.array(image)

# 将RGB值转换为灰度值
if len(image_array.shape) == 3:  # 彩色图像
    gray_image = 0.2989 * image_array[:, :, 0] + 0.5870 * image_array[:, :, 1] + 0.1140 * image_array[:, :, 2]
else:  # 灰度图像
    gray_image = image_array

# 设置阈值
black_threshold = 250 # 黑点阈值

# 检测黑点
black_points = []

for y in range(gray_image.shape[0]):
    for x in range(gray_image.shape[1]):
        brightness = gray_image[y, x]
        if brightness < black_threshold:
            black_points.append((x, y, brightness))

# 创建输出文件夹
output_folder = os.path.splitext(image_path)[0] + "_黑点"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义切片大小
slice_size = 14

# 生成并保存图像切片
def save_slice(point, label):
    x, y, brightness = point
    left = max(x - slice_size // 2, 0)
    right = min(x + slice_size // 2, image_array.shape[1])
    top = max(y - slice_size // 2, 0)
    bottom = min(y + slice_size // 2, image_array.shape[0])

    slice_img = image_array[top:bottom, left:right]
    slice_img_pil = Image.fromarray(slice_img)
    slice_filename = os.path.join(output_folder, f"{label}_x{x}_y{y}_brightness{int(brightness)}.jpg")
    slice_img_pil.save(slice_filename)

# 使用多线程保存黑点切片
with ThreadPoolExecutor() as executor:
    executor.map(lambda point: save_slice(point, "black"), black_points)

# 输出黑点的个数及其坐标
print(f"黑点数量: {len(black_points)}")
for point in black_points:
    print(f"黑点坐标: {point[0]}, {point[1]}, 亮度: {point[2]}")
