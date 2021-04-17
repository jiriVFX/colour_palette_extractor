from flask import Flask, render_template, request, flash, session
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
from forms import ExtractColoursForm
from colour_extractor import ColourExtractor

app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["POST", "GET"])
def home():
    colour_form = ExtractColoursForm()

    if colour_form.validate_on_submit():
        # Remove all previous flash messages
        session.pop("_flashes", None)

        # Save uploaded image ------------------------------------------------------------------------------------------
        file_name = secure_filename(colour_form.file.data.filename)
        file = colour_form.file.data
        path = "static/img/" + file_name
        file.save(path)
        print(path)

        # Retrieve form data -------------------------------------------------------------------------------------------
        colours_num = int(request.form["colours_num"])
        # print(colours_num)
        # precision = request.form["precision"]
        # print(precision)
        # brightness = request.form.get("brightness")
        # print(brightness)
        # gradient = request.form.get("gradient")
        # print(gradient)

        # Create ColourExtractor object --------------------------------------------------------------------------------
        extractor = ColourExtractor()
        extractor.load_image(path)
        extractor.resize_image()
        colours = extractor.extract_colours(colours_num)

        flash("Colours extracted successfully.")
        return render_template("colours.html", form=colour_form, colours=colours, image=path)

    return render_template("colours.html", form=colour_form, colours=None, image=None)


if __name__ == '__main__':
    app.run(debug=True)
