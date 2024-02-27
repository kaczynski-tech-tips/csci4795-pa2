from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess
import random

UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './results'
ALLOWED_EXTENSIONS = {'cc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.call("python3 compex.py > results/res", shell=True)

            return redirect(url_for('download_file', name=filename))

    return render_template("index.html")      

@app.route('/uploads/<name>')
def download_file(name):
    with open('./results/res', 'r') as fs:
        res_out = fs.read()
    
    return render_template("results.html", name=name, res=res_out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
