import os
import pickle

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

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


@app.route('/api/lr', methods=['POST'])
def linear_regression():
    # 判断是预测请求还是训练请求
    request_type = request.args.get('type')

    try:
        # 解析请求数据
        data = request.get_json()

        if request_type == 'train':
            column_x = data['columnX']
            column_y = data['columnY']
            use_intercept = data['useIntercept']
            raw_data = data['data']

            # 将数据转换为pandas DataFrame
            df = pd.DataFrame(raw_data)

            # 检查X列和Y列是否存在
            if not all(x in df.columns for x in column_x) or column_y not in df.columns:
                return jsonify({'error': '所选的列不存在于数据中'}), 400

            # 创建线性回归模型
            lin_reg = LinearRegression(fit_intercept=use_intercept)

            # 训练模型
            X = df[column_x]
            y = df[column_y]
            lin_reg.fit(X, y)

            # 获取回归统计信息
            coefficients = lin_reg.coef_.tolist()
            intercept = lin_reg.intercept_
            score = lin_reg.score(X, y)

            # 保存模型到文件，方便用于预测
            model_path = 'models/lin_reg.pkl'
            if not os.path.exists('models'):
                os.mkdir('models')
            with open(model_path, 'wb') as f:
                pickle.dump(lin_reg, f)

            result = {
                'coefficients': coefficients,
                'intercept': intercept,
                'score': score,
                'message': '线性回归模型训练成功'
            }
            return jsonify(result), 200

        elif request_type == 'predict':
            # 获取预测输入数据
            predict_data = data['predictValues']
            model_path = 'models/lin_reg.pkl'

            print(predict_data)

            # 确保模型文件存在
            if not os.path.exists(model_path):
                return jsonify({'error': '模型尚未训练，请先训练模型'}), 400

            # 加载训练好的模型
            with open(model_path, 'rb') as f:
                print('模型加载成功')
                lin_reg = pickle.load(f)

            # 将预测数据转换为pandas DataFrame
            predict_df = pd.DataFrame([predict_data])
            print(predict_df)
            # 预测
            try:
                prediction = lin_reg.predict(predict_df)
                result = {
                    'prediction': prediction[0],
                    'message': '预测成功完成'
                }
            except Exception as e:
                result = {
                    'error': str(e),
                    'message': '预测失败'
                }

            return jsonify(result), 200

        else:
            return jsonify({'error': '请求类型不明确，应为train或predict'}), 400

    except Exception as e:
        # 异常处理
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
