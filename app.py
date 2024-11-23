# app.py
from flask import Flask, request, render_template
from tensorflow import keras
import numpy as np
import tensorflow as tf
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
model = keras.models.load_model('multi_output_dr_dme_model.keras')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an image was uploaded
    if 'image' not in request.files:
        return render_template('result.html', message='No image uploaded.')
    file = request.files['image']

    if file.filename == '':
        return render_template('result.html', message='No image selected.')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
    else:
        return render_template('result.html', message='Invalid file type.')

    try:
        # Read and preprocess the image
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Make predictions
        preds = model.predict(img_array)
        dr_pred = np.argmax(preds['dr_output'], axis=1)[0]
        dme_pred = int(preds['dme_output'][0][0] > 0.5)

        # Map the predictions to labels
        dr_grades = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']
        dr_result = dr_grades[dr_pred]
        dme_result = 'DME Present' if dme_pred == 1 else 'No DME'

        # Return the results page
        return render_template('result.html', dr_grade=dr_result, dme_presence=dme_result)
    except Exception as e:
        return render_template('result.html', message='Error processing image.')
    finally:
        # Optionally delete the uploaded image to save space
        if os.path.exists(image_path):
            os.remove(image_path)

# New route for the About page
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# New route for the Treatment page
@app.route('/treatment', methods=['GET'])
def treatment():
    return render_template('treatment.html', request=request)

if __name__ == '__main__':
    app.run(debug=True)
