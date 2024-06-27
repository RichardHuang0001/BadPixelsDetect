import os
from PIL import Image, ExifTags
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# 读取图像并解析元信息
image_path = 'IMG_4457.JPG'  # 图片路径
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
noise_threshold = 60  # 噪点阈值
bad_pixel_threshold = 250  # 坏点阈值

# 检测噪点和坏点
noise_points = []
bad_points = []

for y in range(gray_image.shape[0]):
    for x in range(gray_image.shape[1]):
        brightness = gray_image[y, x]
        if brightness > noise_threshold:
            noise_points.append((x, y, brightness))
        if brightness > bad_pixel_threshold:
            bad_points.append((x, y, brightness))

# 创建输出文件夹
output_folder = os.path.splitext(image_path)[0] + "_噪点坏点"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义切片大小
slice_size = 30

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

# 使用多线程保存噪点和坏点切片
with ThreadPoolExecutor() as executor:
    executor.map(lambda point: save_slice(point, "noise"), noise_points)
    executor.map(lambda point: save_slice(point, "bad"), bad_points)

# 输出噪点和坏点的个数及其坐标
print(f"噪点数量: {len(noise_points)}")
for point in noise_points:
    print(f"噪点坐标: {point[0]}, {point[1]}, 亮度: {point[2]}")

print(f"坏点数量: {len(bad_points)}")
for point in bad_points:
    print(f"坏点坐标: {point[0]}, {point[1]}, 亮度: {point[2]}")
