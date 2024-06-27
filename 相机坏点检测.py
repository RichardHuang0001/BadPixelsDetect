from PIL import Image, ExifTags
import numpy as np

# 读取图像并解析元信息
image_path = 'IMG_4459.JPG'  # 替换为实际的图像路径
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
noise_threshold = 60 # 噪点阈值
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

# 输出噪点和坏点的个数及其坐标
print(f"噪点数量: {len(noise_points)}")
for point in noise_points:
    print(f"噪点坐标: {point[0]}, {point[1]}, 亮度: {point[2]}")

print(f"坏点数量: {len(bad_points)}")
for point in bad_points:
    print(f"坏点坐标: {point[0]}, {point[1]}, 亮度: {point[2]}")
