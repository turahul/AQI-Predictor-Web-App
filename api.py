from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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

def model_predict(img_path,model,filename):
    
    
    img = cv2.imread(img_path)
    img = cv2.resize(img, (96, 96))
    img = img.astype("float") / 255.0
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    K.clear_session()
    y_classes = prediction.argmax(axis=1) 
    save(y_classes,filename)
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
            print(image.filename)
            image.save(file_path)
            # Make prediction
            model = load_model(model_path)
            model.load_weights(model_weight)
            preds = model_predict(file_path, model,image.filename)
            
            '''
            file = os.getcwd()
            del_pic = file +'\\uploads\\'+filename
            os.remove(del_pic)
            print(os.getcwd())
            '''
            return str(preds)
            
    return "Error"
def save(value,filename):

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentialsPersonalDrive.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    
    folder_id = '1tBCT11Y2UAkD6esgrN_39xymzz6hyMhD' 
    names = str(value) + '.png'
    file_metadata = {
        'name': [names],
        'parents': [folder_id]
    }
    read = 'uploads/' + filename
    media = MediaFileUpload(read,
                            mimetype='image/jpeg',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))
    

if __name__ == '__main__':
    app.run(debug=True)    