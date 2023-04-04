from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './imageSegmentation/input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
OUTPUT_FOLDER = './imageSegmentation/output'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path_output = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            file.save(file_path)


            os.system("python ./imageSegmentation/inference.py --jit_path ./imageSegmentation/DMS46_v1.pt --image_folder ./imageSegmentation/input --output_folder ./imageSegmentation/output")

            # 打开并裁剪图片的右半部分
            image = Image.open(file_path_output)
            width, height = image.size
            cropped_image = image.crop((width // 2, 0, width, height))
            cropped_image.save(file_path_output)

            # 将裁剪后的图片保存到内存中
            output = io.BytesIO()
            cropped_image.save(output, format='JPEG')
            output.seek(0)

            # 将裁剪后的图片发送回前端
            return send_file(output, mimetype='image/jpeg')
        else:
            return {'status': 'error', 'message': 'No file uploaded'}

if __name__ == '__main__':
    app.run()




# flask --app hello.py run
