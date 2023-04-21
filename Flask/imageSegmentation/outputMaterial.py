import json
import os
import cv2
import numpy as np
import pandas as pd
import sys
from PIL import Image

def load_lookup_table(file_path):
    with open(file_path, 'rb') as f:
        lookup_data = json.load(f)
    return lookup_data['lookup_table']

def get_material_name_by_color(color, lookup_table):
    for item in lookup_table:
        if item['Color'] == color.tolist():
            return item['Short Name']
    return None

def get_material_color_by_name(name, lookup_table):
    for item in lookup_table:
        if item['Short Name'] == name:
            return item['Color']
    return None

def process_segmented_image(image_path, lookup_table):
    image = cv2.imread(image_path)
    # print(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if image is None:
        print(f"无法读取图像：{image_path}")
        sys.exit(1)
    #这步返回的颜色正确
    unique_colors = np.unique(image.reshape(-1, image.shape[-1]), axis=0)
    
    # print(unique_colors)  #这步返回的颜色正确
    total_pixels = image.shape[0] * image.shape[1]

    materials = {}
    for color in unique_colors:
        # print(color)   #这步是对的
        material_name = get_material_name_by_color(color, lookup_table)
        if material_name:
            if material_name not in materials:
                materials[material_name] = 0
            materials[material_name] += np.count_nonzero(np.all(image == color, axis=-1))

    materials_percent = {k: v / total_pixels * 100 for k, v in materials.items()}
    # print(unique_colors,materials_percent)
      #这步返回的颜色正确
    return unique_colors, materials, materials_percent

def save_output_image(output_path, unique_colors, materials, materials_percent, lookup_table):
    image = np.zeros((len(unique_colors) * 40 + 50, 500, 3), dtype=np.uint8)

    for i, color in enumerate(unique_colors):
        # print(color)  # 这步是对的
        # print(i)
        material_name = get_material_name_by_color(color, lookup_table)
        # print(lookup_table)
        print(material_name)
        if material_name:
            percent = materials_percent[material_name]
            # print(percent)
            # color = lookup_table[i]['Color']
            color = get_material_color_by_name(material_name,lookup_table)
            # print(color)
            # 这步是对的
            label = f"{material_name} ({percent:.2f}% {color})"
            color = np.array(color)
            rgb_color = color.tolist()
            bgr_color = rgb_color[::-1]  # 将颜色列表反转，得到 BGR 顺序的颜色值
            image = cv2.putText(image, label, (20, 40*(i+1)), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr_color, 2)
            image = cv2.rectangle(image, (200, 40*i+10), (295, 40*i+30), bgr_color, -1)
            # image = cv2.putText(image, f"{pixels:,d} pixels", (200, 40*i+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    cv2.imwrite(output_path, image)

def crop_and_replace_images(segmented_images_dir):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    for filename in os.listdir(segmented_images_dir):
        file_path = os.path.join(segmented_images_dir, filename)
        file_extension = os.path.splitext(filename)[-1].lower()

        if not os.path.isfile(file_path) or file_extension not in valid_extensions:
            continue
        
        # 打开图像
        image = Image.open(file_path)
        
        # 计算裁剪区域
        width, height = image.size
        crop_area = (width // 2, 0, width, height)
        
        # 裁剪图像
        cropped_image = image.crop(crop_area)
        
        # 保存裁剪后的图像，替换原图像
        cropped_image.save(file_path)

def process_segmented_images_and_fill_to_csv(csv_path, segmented_images_dir,segmented_images_output, lookup_table_path):
    # 读取csv文件
    df = pd.read_csv(csv_path)

    # 读取lookup table和生成列名
    with open(lookup_table_path, 'rb') as f:
        lookup_data = json.load(f)
    lookup_table = lookup_data['lookup_table']
    material_names = [item['Short Name'] for item in lookup_table]
    for material_name in material_names:
        df[material_name] = 0

    # 遍历分割图片并填充对应的材料数量
    segmented_images = [f for f in os.listdir(segmented_images_dir) if f.endswith('.jpg') or f.endswith('.png')]
    for image_name in segmented_images:
        image_path = os.path.join(segmented_images_dir, image_name)
        name, ext = os.path.splitext(image_name)
        # print(name)
        output_path = os.path.join(segmented_images_dir, f"{name}_with_labels{ext}")
        unique_colors, materials, materials_percent = process_segmented_image(image_path, lookup_table)
        # 将分割结果填充到csv中
        intname = int(name)
        row_idx = df.index[df['SVI_ID'] == intname][0]
        print(row_idx)
        for material_name, percentage in materials_percent.items():
            print(f"{material_name}: {percentage:.2f}%")
            df.at[row_idx, material_name] = percentage/100
            

        name, ext = os.path.splitext(image_name)
        output_path = os.path.join(segmented_images_output, f"{name}_with_labels{ext}")
        save_output_image(output_path, unique_colors, materials, materials_percent, lookup_table)

    # 保存csv文件
    new_csv_path = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/Data/Columbia_SVIpoints_4326_output.csv'
    df.to_csv(new_csv_path, index=False)

lookup_table_path = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/output_lookup_table.json'
lookup_table = load_lookup_table('/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/output_lookup_table.json')

segmented_images_output = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/testMaterialType/testMaterialTypeOutput'

segmented_images_dir = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/testMaterialType'
segmented_images = [f for f in os.listdir(segmented_images_dir) if f.endswith('.jpg') or f.endswith('.png')]
csv_path = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/Data/Columbia_SVIpoints_4326.csv'

crop_and_replace_images(segmented_images_dir)

process_segmented_images_and_fill_to_csv(csv_path, segmented_images_dir,segmented_images_output, lookup_table_path)