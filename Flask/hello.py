from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # 允许所有域名访问

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask API!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run()


# flask --app hello.py run
