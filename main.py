import os
from werkzeug.utils import secure_filename
from color_picker import ColorPicker
from flask import Flask, render_template, redirect, request, flash
from datetime import datetime
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['UPLOAD_FOLDER']="./static/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class AddImage(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])
    submit = SubmitField("Show Colors")


def allowed_file(filename):
    if '.' not in filename:
        flash('File has no extension')
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        flash(f'File format must be one of: {", ".join(ALLOWED_EXTENSIONS)}')
        return False
    return True


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route("/", methods=["GET", "POST"])
def home():
    form = AddImage()
    filename = ""
    palette = []
    if form.validate_on_submit():
        # Delete previous images
        for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print("Error deleting file:", e)
        # Check if file is image, if it has correct extension
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = form.image.data
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Add file in folder and get colors from Class ColorPicker
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = ColorPicker("./static/images/" + filename)
            rest_colors = img.palette
            for color in rest_colors:
                palette.append(color)
            return render_template("index.html", form=form, filename=filename,
                                   palette=palette)
    return render_template("index.html", form=form, filename=filename, palette=palette)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
