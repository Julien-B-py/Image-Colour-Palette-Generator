import base64
import io
import os

from PIL import Image
from flask import Flask, render_template, flash, jsonify, request
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from werkzeug.utils import secure_filename

from forms import UploadImage
from image import IMG
from utils import allowed_file

# Create a boolean which will be set to True if the app is running online on Heroku
running_on_heroku = False
if 'HEROKU_DEPLOY_VAR' in os.environ:
    running_on_heroku = True

# Specify the path where the app will store the uploaded files depending on the app location (online or local)
if running_on_heroku:
    UPLOAD_FOLDER = '/tmp/'
    print('ONLINE MODE')
else:
    UPLOAD_FOLDER = r'static\uploads'
    print('LOCAL MODE')

app = Flask(__name__)
CORS(app)

# Setup secret key to keep the client-side sessions secure.
SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Specify the path where the app will store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Specify the max file size that can be uploaded
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 3MB

Bootstrap(app)

settings = {"delta": 0, "nb_colors": 0}


@app.route("/", methods=["GET", "POST"])
def analyse_image():
    # Create a WTForm with default values 10 and 24
    form = UploadImage(nb_colors=10, delta=24)

    if form.validate_on_submit():

        image_file = form.image_file.data
        nb_colors = form.nb_colors.data
        delta = form.delta.data

        print(image_file)

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

                # If app is online saves the image contents in memory to pass image data to the template
                if running_on_heroku:
                    data = io.BytesIO()
                    image.image.save(data, "JPEG")
                    encoded_img_data = base64.b64encode(data.getvalue())
                    img_data = encoded_img_data.decode('utf-8')
                else:
                    img_data = None

                # Get list of dict containing the most common colors including rgb, hex and percentage values
                top_colors = image.analyze()

                # Get the img color palette by ignoring similar colors and sort it from the darkest to the lighter color
                color_palette = image.get_color_palette(delta=delta, nb_colors=nb_colors)

                # Slice top_colors to only display the 20 most common colors of the image
                return render_template('results.html', top_colors=top_colors[:20], img_data=img_data, filename=filename,
                                       color_palette=color_palette)

        # If file extension is not authorized
        flash('This file is not valid, please select an image')

    return render_template('upload.html', form=form)


# API ROUTES

@app.route("/api/upload", methods=["POST"])
def upload():
    nb_colors = settings.get("nb_colors")
    delta = settings.get("delta")

    file = request.files
    image_file = file.get('my-image-file')

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

            # If app is online saves the image contents in memory to pass image data to the template
            if running_on_heroku:
                try:
                    data = io.BytesIO()
                    image.image.save(data, "JPEG")
                    encoded_img_data = base64.b64encode(data.getvalue())
                    img_data = encoded_img_data.decode('utf-8')
                except KeyError:
                    return 'PNG files with transparency are not supported.', 500

            else:
                img_data = None

            # Get list of dict containing the most common colors including rgb, hex and percentage values
            try:
                top_colors = image.analyze()
            except ValueError:
                return 'PNG files with transparency are not supported.', 500

            # Get the img color palette by ignoring similar colors and sort it from the darkest to the lighter color
            color_palette = image.get_color_palette(delta=delta, nb_colors=nb_colors)

            # Edit for React app (remove rgb from dict : couldnt jsonify)
            # Slice top_colors to only display the 20 most common colors of the image
            top_20_colors = []
            for color in top_colors[:20]:
                edited_color = {'hex': color.get('hex'), 'ratio': color.get('ratio')}
                top_20_colors.append(edited_color)

            return jsonify(top_20_colors=top_20_colors, img_data=img_data, filename=filename,
                           color_palette=color_palette)


    return 'Make sure you submitted an image.', 500


@app.route("/api/settings", methods=["POST"])
def setup():
    data = request.get_json()
    settings["delta"] = data.get("delta")
    settings["nb_colors"] = data.get("nb_colors")

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
