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

Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def analyse_image():
    # Create a WTForm
    form = UploadImage()

    if form.validate_on_submit():

        image_file = form.image_file.data

        if allowed_file(image_file.filename):

            # Always use that function to secure a filename (Flask doc)
            filename = secure_filename(image_file.filename)
            # If a file has been uploaded, store it in the upload folder
            if filename:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                image_file.save(image_path)

                image = IMG(image_path)
                top_colors = image.analyse(colors=200)

                ### TEST CLEANUP

                to_clean = top_colors.copy()
                print(to_clean)
                clean = []

                while to_clean:

                    current_color = to_clean[0]

                    too_close = False

                    r = current_color['rgb'][0]
                    g = current_color['rgb'][1]
                    b = current_color['rgb'][2]

                    if clean:
                        for color_2 in clean:
                            r_2 = color_2[0]
                            g_2 = color_2[1]
                            b_2 = color_2[2]

                            if abs(int(r) - int(r_2)) <= 24 and abs(int(g) - int(g_2)) <= 24 and abs(
                                    int(b) - int(b_2)) <= 24:
                                too_close = True

                        if not too_close:
                            clean.append((r, g, b))


                    if not clean:
                        clean.append((r, g, b))

                    del to_clean[0]

                print(clean)

                color_palette = []
                for value in clean:
                    r=value[0]
                    g = value[1]
                    b = value[2]
                    color_palette.append(f'#{convert_to_hex(r)}{convert_to_hex(g)}{convert_to_hex(b)}')

                print(color_palette)

                ### FIN TEST

                return render_template('results.html', top_colors=top_colors, filename=filename, color_palette=color_palette)

        flash('This file is not valid, please select an image')

    return render_template('upload.html', form=form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
