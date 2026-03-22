import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATHS = {
    "apple": os.path.join(BASE_DIR, "apple_model.h5"),
    "tomato": os.path.join(BASE_DIR, "tomato_model.h5"),
    "potato": os.path.join(BASE_DIR, "potato_model.h5"),
    "corn": os.path.join(BASE_DIR, "corn_model.h5"),
}

LABEL_PATHS = {
    "apple": os.path.join(BASE_DIR, "apple.txt"),
    "tomato": os.path.join(BASE_DIR, "tomato.txt"),
    "potato": os.path.join(BASE_DIR, "potato.txt"),
    "corn": os.path.join(BASE_DIR, "corn.txt"),
}


def load_labels(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def predict_disease(img_path, crop):

    if crop not in MODEL_PATHS:
        return "Model not available for this crop"

    model = tf.keras.models.load_model(MODEL_PATHS[crop], compile=False)
    labels = load_labels(LABEL_PATHS[crop])

    img = load_img(img_path, target_size=(256,256))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)

    confidence = np.max(prediction) * 100
    return f"{labels[predicted_class]} ({confidence:.2f}%)"