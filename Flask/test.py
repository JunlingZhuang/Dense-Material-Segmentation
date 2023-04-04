import os
os.system("python ./imageSegmentation/inference.py --jit_path ./imageSegmentation/DMS46_v1.pt --image_folder ./imageSegmentation/input --output_folder ./imageSegmentation/output")
