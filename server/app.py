import numpy as np
from scipy.stats import pearsonr
from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        data = None
        if filename.endswith('.csv'):
            try:
                data = pd.read_csv(filename).reset_index(drop=True)
            except Exception as e:
                return jsonify(error="Unable to read CSV file"), 400
        else:
            try:
                data = pd.read_excel(filename).reset_index(drop=True)
            except Exception as e:
                # return jsonify(error="Unable to read Excel file"), 400
                return jsonify(error=e), 400

        data = data.dropna(axis=1, how='all')  # 丢弃nan的值
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]  # 丢弃没有列名的列

        # print(data)

        return jsonify(data=data.to_dict(orient='records'))

    return jsonify(error="Invalid file type"), 400


@app.route('/api/stats', methods=['POST'])
def get_stats():
    req_data = request.get_json()
    # print(req_data)
    # 检查请求数据是否存在
    if not req_data:
        return jsonify({"error": "Request data is empty or not JSON"}), 400

    column = req_data.get('column')
    data = req_data.get('data')

    # 检查column键是否存在
    if not column:
        return jsonify({"error": "Column is required"}), 400

    # 检查data键是否存在
    if not data:
        return jsonify({"error": "Data is required"}), 400

    # 检查data是否为列表
    if not isinstance(data, list):
        return jsonify({"error": "Data should be a list"}), 400

    # 检查列表中的项目是否为字典
    if not all(isinstance(item, dict) for item in data):
        return jsonify({"error": "All items in data should be dictionaries"}), 400

    try:
        # 获取具有有效数值类型的数据列
        values = [item.get(column) for item in data if isinstance(item.get(column), (int, float))]

        if not values:
            return jsonify({"error": "Column not found in data or contains no valid numeric data"}), 404

        values = np.array(values)
        mean = np.mean(values)
        median = np.median(values)
        minimum = np.min(values)
        maximum = np.max(values)
        quartiles = np.percentile(values, [25, 50, 75])

        return jsonify({
            "mean": mean.item(),
            "median": median.item(),
            "min": minimum.item(),
            "max": maximum.item(),
            "quartiles": quartiles.tolist(),
        })
    except Exception as e:
        # 详细错误消息将帮助调试
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/api/correlation', methods=['POST'])
def calculate_correlation():
    data = request.get_json()
    # print(data)
    # 假设发送的数据是一个字典，包含两个键：column1 和 column2，它们都对应着数据列表
    column1 = data.get('column1')
    column2 = data.get('column2')
    if not (column1 and column2):
        return jsonify({'error': 'Invalid input data'}), 400

    if len(column1) != len(column2):
        return jsonify({'error': 'Columns must be of the same length'}), 400

    try:
        # 计算相关系数
        correlation, _ = pearsonr(column1, column2)
        return jsonify({'correlation': correlation}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
