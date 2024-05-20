from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from controller.controller import safe_homework

# Erstellen Sie einen Blueprint
routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = 'uploads'

@routes.route('/', methods=['GET'])
def home():
    return safe_homework(request)  

@routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
