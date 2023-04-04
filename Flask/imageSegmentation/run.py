import os


# os.chdir('/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation')
# os.system("python inference.py --jit_path ./DMS46_v1.pt --image_folder ./input --output_folder ./output")
os.system("python ./inference.py --jit_path ./DMS46_v1.pt --image_folder ./input --output_folder ./output")