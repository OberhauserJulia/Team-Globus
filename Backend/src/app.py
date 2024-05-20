from flask import Flask
import os

# Importieren Sie den Blueprint
from routes.routes import routes

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Registrieren Sie den Blueprint
app.register_blueprint(routes)
