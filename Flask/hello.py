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
         
            # Get the names of all files in the specified folder
            filenames = os.listdir(app.config['SVIIMAGES_FOLDER'])

            # Extracts the numeric part of a file name using a regular expression and sorts the file name by the numeric part
            pattern = re.compile(r'^(\d+)(\.[a-zA-Z]+)$')
            numbers = []
            for filename in filenames:
                match = pattern.match(filename)
                if match:
                    number = int(match.group(1))
                    numbers.append(number)

            if len(numbers) > 0:
                # Sort the names of successfully matched files and calculate the new numeric part
                numbers_sorted = sorted(numbers)
                new_number = numbers_sorted[-1] + 1

                # Combine the numeric part and the specified suffix (e.g. .jpg) into a new file name
                new_filename = str(new_number) + ".jpg"

                # Combine the new file name and destination folder path, for example"/path/to/destination/600.jpg"
                file_path_SVI_new = os.path.join(app.config['SVIIMAGES_FOLDER'], new_filename)

                # Combine the numeric part and the specified suffix (e.g. .jpg) into a new file name
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
            file.seek(0)  # Resetting the file pointer to the beginning of the file
            file.save(file_path_SVI)


           
            os.system("python ./imageSegmentation/inference.py --jit_path ./imageSegmentation/DMS46_v1.pt --image_folder ./imageSegmentation/input --output_folder ./imageSegmentation/output")

            # Open and crop the right half of the image
            image = Image.open(file_path_output)
            width, height = image.size
            cropped_image = image.crop((width // 2, 0, width, height))
            cropped_image.save(file_path_output)

            # Store SVI Segementation image to frontend folder
            cropped_image.save(file_path_SVI_output)

            # Save the cropped image to memory
            output = io.BytesIO()
            cropped_image.save(output, format='PNG')
            output.seek(0)

            # Send the cropped image back to the front end
            return send_file(output, mimetype='image/png')
        else:
            return {'status': 'error', 'message': 'No file uploaded'}

if __name__ == '__main__':
    app.run()




# flask --app hello.py run
