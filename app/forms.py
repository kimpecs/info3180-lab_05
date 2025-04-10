# Add any form classes for Flask-WTF here

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Poster', validators=[
        DataRequired(),
        # Custom validator for image files
        lambda _, field: isinstance(field.data, FileStorage) and \
            '.' in field.data.filename and \
            field.data.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
    ])