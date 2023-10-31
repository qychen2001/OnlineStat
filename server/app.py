import numpy as np
from tabnanny import filename_only
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

        return jsonify(data=data.to_dict(orient='records'))

    return jsonify(error="Invalid file type"), 400


@app.route('/api/stats', methods=['POST'])
def get_stats():
    req_data = request.get_json()
    column = req_data.get('column')
    data = req_data.get('data')

    if not column:
        return jsonify({"error": "Column is required"}), 400

    if not data:
        return jsonify({"error": "Data is required"}), 400

    try:
        values = [item[column] for item in data if column in item and isinstance(
            item[column], (int, float))]
        if not values:
            return jsonify({"error": "Column not found in data or invalid data type"}), 404

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
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
