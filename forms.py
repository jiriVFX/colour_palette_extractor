from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


# WTForm
class ExtractColoursForm(FlaskForm):
    file = FileField("", validators=[FileRequired(), FileAllowed(["jpg", "png"], "Select image file!")])
    colours_num = IntegerField("Number of colours to extract", validators=[DataRequired()])
    submit = SubmitField("Extract colours")

