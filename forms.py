from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadImage(FlaskForm):
    """A WTForm for uploading an image"""
    image_file = FileField('Select an image to get his corresponding color palette', validators=[DataRequired()])
    submit = SubmitField("Submit image")
