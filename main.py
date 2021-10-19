import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from forms import UploadImage
from image import IMG

SECRET_KEY = os.environ.get('SECRET_KEY')
# Specify the path where the app will store the uploaded files
UPLOAD_FOLDER = r'static\uploads'

app = Flask(__name__)

# Setup secret key to keep the client-side sessions secure.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Specify the path where the app will store the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def analyse_image():
    # Create a WTForm
    form = UploadImage()

    if form.validate_on_submit():

        image_file = form.image_file.data
        # Always use that function to secure a filename (Flask doc)
        filename = secure_filename(image_file.filename)
        # If a file has been uploaded, store it in the upload folder
        if filename:
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            image = IMG(image_path)
            top_colors = image.analyse(colors=50)

            return render_template('results.html', top_colors=top_colors, filename=filename)

    return render_template('upload.html', form=form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
