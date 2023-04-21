from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import os
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FOLDER = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Dense-Material-Segmentation/Flask/imageSegmentation/output'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

SVIIMAGES_FOLDER = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Materiafolio/materialfolio/public/SVI_Images'
app.config['SVIIMAGES_FOLDER'] = SVIIMAGES_FOLDER

SEGEMENTIMAGES_FOLDER = '/Users/zhuangjunling/Documents/GitHub/GSAPP/Materiafolio/materialfolio/public/Segemented_Images'
app.config['SEGEMENTIMAGES_FOLDER'] = SEGEMENTIMAGES_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
         

                    
            # 获取指定文件夹下的所有文件名
            filenames = os.listdir(app.config['SVIIMAGES_FOLDER'])

            # 使用正则表达式提取文件名中的数字部分，并将文件名按照数字部分进行排序
            pattern = re.compile(r'^(\d+)(\.[a-zA-Z]+)$')
            numbers = []
            for filename in filenames:
                match = pattern.match(filename)
                if match:
                    number = int(match.group(1))
                    numbers.append(number)

            if len(numbers) > 0:
                # 对成功匹配的文件名进行排序，并计算新的数字部分
                numbers_sorted = sorted(numbers)
                new_number = numbers_sorted[-1] + 1

                # 将数字部分和指定的后缀名（如.jpg）组合成新的文件名
                new_filename = str(new_number) + ".jpg"

                # 组合新文件名和目标文件夹路径，例如"/path/to/destination/600.jpg"
                file_path_SVI_new = os.path.join(app.config['SVIIMAGES_FOLDER'], new_filename)

                # 打印新文件名和路径
                print(new_filename)



            filename = file.filename
            print(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file_path_output = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(new_filename)[0] + ".png")

            # Handle frontend foloer path
            file_path_SVI = os.path.join(app.config['SVIIMAGES_FOLDER'], new_filename)
            file_path_SVI_output = os.path.join(app.config['SEGEMENTIMAGES_FOLDER'], os.path.splitext(new_filename)[0] + ".png")

            # print(file_path_output)
            # print(file_path_SVI_output)
            file.save(file_path)

            # Store Orignial SVI image to frontend folder
            file.seek(0)  # 将文件指针重新设置到文件开头
            file.save(file_path_SVI)


           
            os.system("python ./imageSegmentation/inference.py --jit_path ./imageSegmentation/DMS46_v1.pt --image_folder ./imageSegmentation/input --output_folder ./imageSegmentation/output")

            # 打开并裁剪图片的右半部分
            image = Image.open(file_path_output)
            width, height = image.size
            cropped_image = image.crop((width // 2, 0, width, height))
            cropped_image.save(file_path_output)

            # Store SVI Segementation image to frontend folder
            cropped_image.save(file_path_SVI_output)

            # 将裁剪后的图片保存到内存中
            output = io.BytesIO()
            cropped_image.save(output, format='PNG')
            output.seek(0)

            # 将裁剪后的图片发送回前端
            return send_file(output, mimetype='image/png')
        else:
            return {'status': 'error', 'message': 'No file uploaded'}

if __name__ == '__main__':
    app.run()




# flask --app hello.py run
