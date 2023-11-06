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



@app.route('/api/corr', methods=['POST'])
def calculate_correlation():
    try:
        data = request.get_json()

        if not data:
            raise ValueError("没有提供数据。")

        # 从数据中获取 column1 和 column2 的名称
        column1_name = data.get('column1')
        column2_name = data.get('column2')

        # 获取传入的数据集
        origin_data = pd.DataFrame.from_dict(data.get('data'))

        if column1_name is None or column2_name is None:
            raise ValueError("缺少必要的数据列名称。")

        # 检查传入的数据中是否有这两列
        if column1_name not in origin_data.columns or column2_name not in origin_data.columns:
            raise ValueError("指定的列名在数据中不存在。")

        # 计算相关系数
        corr_coefficient, _ = pearsonr(origin_data[column1_name], origin_data[column2_name])

        # 返回结果
        return jsonify({
            'correlation': corr_coefficient
        })

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        # 对于不是由 ValueError 引发的其他任何异常，我们返回500内部服务器错误
        return jsonify({'error': '服务器内部错误: {}'.format(str(e))}), 500


if __name__ == '__main__':
    app.run(debug=True)
