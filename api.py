from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import cv2
#from flask_cors import CORS
import numpy as np
import os
#import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras import backend as K

app = Flask(__name__)
#CORS(app)

model_path = "Static/Model/VGG16.h5" 
model_weight = "Static/Model/weights_VGG16.h5"

@app.route('/')   
@app.route('/Home.html')
def home():
    return render_template('Home.html',
                       title='Home')
    
@app.route('/AboutUs.html')
def AboutUs():
    return render_template('AboutUs.html')
    
@app.route('/aqiTeller.html')
def aqiTeller():
    return render_template('aqiTeller.html')
    
@app.route('/Contact.html')
def contact():
    return render_template('Contact.html')
    
@app.route('/Map.html')
def map():
    return render_template('Map.html')  

def model_predict(img_path, model):    
    img = cv2.imread(img_path)
    img = cv2.resize(img, (96, 96))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    K.clear_session()
    y_classes = prediction.argmax(axis=1) 
    return y_classes
    
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":

        if request.files:
            output={}
            image = request.files["image"]
            print(request.files)
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
            basepath, 'uploads', secure_filename(image.filename))
            image.save(file_path)
            print(file_path)
            # Make prediction
            model = load_model(model_path)
            model.load_weights(model_weight)
            preds = model_predict(file_path, model)
            
            return str(preds)
            
    return render_template('AboutUs.html')

if __name__ == '__main__':
    app.run(debug=True)    