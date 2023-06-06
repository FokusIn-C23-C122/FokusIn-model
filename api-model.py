from flask import Flask, request, jsonify, make_response
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
#from keras.preprocessing import load_img
from PIL import Image
#from keras.preprocessing import img_to_array, load_img
#from keras.utils import img_to_array, load_img
import numpy as np
import os

varian_dict = {'Fokus' : 0, 'TidakFokus':1}

model = tf.keras.models.load_model("1685871676.h5")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './imagereq/'

def predict_image(img_path):

    img = tf.keras.utils.load_img(img_path, target_size = (224, 224))

    img_array = tf.keras.utils.img_to_array(img)
    img_array = img_array/255.
    img_array = tf.expand_dims(img_array,0)

    varian_list = list(varian_dict.keys())
    prediction = model(img_array)
    pred_idx = np.round(model.predict(img_array)[0][0]).astype('int')
    pred_varian = varian_list[pred_idx]
    return pred_varian

@app.route('/predict', methods=['POST'])
def API():
    if request.method == 'POST':
        if request.json is None :
            return jsonify({"error":"no image"})
        try :
            filejson = request.get_json()
            imageName = filejson["image"]
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], imageName)
            output_image = predict_image(img_path)
            return make_response(jsonify({"predict_image": output_image}), 201)
        except FileNotFoundError as e :
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e :
            print(e)
            return make_response(jsonify({"error": str(e)}), 500)
    return "OK"

if __name__ == "__main__" :
    app.run(debug=True)