from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


# WTForm
class ExtractColoursForm(FlaskForm):
    file = FileField("", validators=[FileRequired(), FileAllowed(["jpg", "png"], "Select image file!")])
    colours_num = IntegerField("Number of colours to extract", validators=[DataRequired()])
    # precision = IntegerField("Precision", validators=[DataRequired()])
    # brightness = BooleanField("Reduce brightness")
    # gradient = BooleanField("Reduce gradient")
    # brightness = RadioField(
    #     "Reduce brightness",
    #     choices=[("brightness_yes", "Yes"), ("brightness_no", "No")],
    #     default="brightness_yes",
    #     validators=[DataRequired()]
    # )
    # gradient = RadioField(
    #     "Reduce gradient",
    #     choices=[("gradient_yes", "Yes"), ("gradient_no", "No")],
    #     default="gradient_yes",
    #     validators=[DataRequired()]
    # )
    submit = SubmitField("Extract colours")



# <!--                    <p>-->
# <!--                      <label for="precision">Precision</label><br />-->
# <!--                      <input type="number" name="precision" class="form-control" step="1" />-->
# <!--                    </p>-->
# <!--                    <p>{{ form.brightness.label }} <br /> {{ form.brightness(class_="radio-group", size=30) }}</p>-->
# <!--                    <p>{{ form.gradient.label }} <br /> {{ form.gradient(class_="radio-group", size=30) }}</p>-->
