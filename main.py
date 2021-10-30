import os

from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from forms import UploadImage
from image import IMG
from utils import allowed_file, convert_to_hex

SECRET_KEY = os.environ.get('SECRET_KEY')
# Specify the path where the app will store the uploaded files
UPLOAD_FOLDER = r'static\uploads'

app = Flask(__name__)

# Setup secret key to keep the client-side sessions secure.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Specify the path where the app will store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Specify the max file size that can be uploaded
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 3MB

Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def analyse_image():
    # Create a WTForm
    form = UploadImage()

    if form.validate_on_submit():

        image_file = form.image_file.data

        # If file extension is in the whitelist allow upload
        if allowed_file(image_file.filename):

            # Always use that function to secure a filename (Flask doc)
            filename = secure_filename(image_file.filename)
            # If a file has been uploaded, store it in the upload folder
            if filename:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)

                # Image color analyze and color palette extraction
                image = IMG(image_path)


                # # Get list of dict containing the 250 most common colors including rgb, hex and percentage values
                # top_colors = image.analyze(colors=250)

                top_colors_1 = image.analyze_new(nb_colors=1000)


                # # Get the img color palette by ignoring similar colors and sort it from the darkest to the lighter color
                # color_palette = image.get_color_palette()


                color_palette = image.get_color_palette_new()


                print('MAIN')
                print(top_colors_1)
                print(filename)
                print(color_palette)

                top_colors = [value for _,value in top_colors_1.items()]

                return render_template('results.html', top_colors=top_colors[:20], filename=filename,
                                       color_palette=color_palette)

        # If file extension is not authorized
        flash('This file is not valid, please select an image')

    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
