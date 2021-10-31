from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class UploadImage(FlaskForm):
    """A WTForm for uploading an image"""
    image_file = FileField('Select an image to get his corresponding color palette', validators=[DataRequired()])
    nb_colors = IntegerField('Number of colors (5-10): ', validators=[DataRequired(), NumberRange(min=5, max=10)])
    delta = IntegerField('Delta (1-255): ', validators=[DataRequired(), NumberRange(min=1, max=255)])
    submit = SubmitField("Submit image")
