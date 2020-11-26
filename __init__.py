from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os

image_folder = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = image_folder
app.config['SECRET_KEY'] = 'NJSNJnnJSNJNSSSKMSKMksmMSKKMSsvfmfvmkf'


class Field(FlaskForm):
    short_url_field = StringField('', validators=[DataRequired()])