import os
from io import BytesIO

from flask import Flask, request, jsonify, make_response
import tensorflow as tf
from PIL import Image
import numpy as np
from urllib import request as urequest

varian_dict = {'Fokus': 0, 'TidakFokus': 1}

model = tf.keras.models.load_model("fokusin_model.h5")

app = Flask(__name__)


def predict_image(img_path):
    res = urequest.urlopen(img_path).read()
    img = Image.open(BytesIO(res)).resize((224, 224))

    img_array = tf.keras.utils.img_to_array(img)
    img_array = img_array / 255.
    img_array = tf.expand_dims(img_array, 0)

    varian_list = list(varian_dict.keys())
    prediction = model(img_array)
    pred_idx = float(model.predict(img_array)[0][0])
    # pred_varian = varian_list[pred_idx]
    return pred_idx


@app.route('/predict', methods=['POST'])
def API():
    if request.method == 'POST':
        if request.json is None:
            return jsonify({"error": "no image"})
        try:
            data = request.json
            img_path = data['image_url']
            output_image = predict_image(img_path)
            return make_response(jsonify({"predict_image": output_image}), 201)
        except FileNotFoundError as e:
            return make_response(jsonify({"error": str(e)}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({"error": str(e)}), 500)
    return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
