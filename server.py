import numpy as np
from flask import Flask, request, redirect, url_for, flash, send_from_directory
import os, io
import cv2
from utils import img_resize
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_name, ext = filename.rsplit('.', 1)
            in_memory_file = io.BytesIO()
            file.save(in_memory_file)   
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            img = img_resize(data)

            if ext.lower() != "jpg" or ext.lower() != "jpeg":
                filename = path_name + '.jpg'
                
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], filename), img,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 20])

            return redirect(url_for('uploaded_file',    
                                    filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Image Resizing</h1>
        <h2>Upload Image</h2>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)