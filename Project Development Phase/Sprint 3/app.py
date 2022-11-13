from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os
import urllib.request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np

model=load_model(r'models/mnistCNN.h5')

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
      
    return render_template("index.html")

@app.route('/recognise', methods=['GET','POST'])
def recognise():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('recognise.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) 
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        flash('Image uploaded successfully')
        img=Image.open(file.stream).convert("L")
        img=img.resize((28,28))
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1,28,28,1)
        y_pred = model.predict(im2arr)
        print(np.argmax(y_pred))
        prediction=str(np.argmax(y_pred))
        
        return render_template('recognise.html',filename=filename,prediction=prediction) 
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url) 

@app.route('/display/<filename>')
def display_image(filename):
    
    return redirect(url_for('static',filename='uploads/' +filename), code=301)

    
if __name__ == "__main__":
    app.run(debug = False)

