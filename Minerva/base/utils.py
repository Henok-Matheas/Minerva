from .apps import BaseConfig
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing import image as img_utils
import numpy as np
from preview_generator.manager import PreviewManager
from thumbnail import generate_thumbnail
import os
from pathlib import Path

book_format_list = [".pdf", ".docx", ".odt"]
video_format_list = [".mp4", ".mkv"]
format_dict = {
    ".pdf": "book",
    ".docx": "book",
    ".odt": "book",
    ".mp4": "video",
    ".mkv": "video"
}
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


def thumbnailer(file):
    for format in book_format_list:
        if str(file).endswith(format):
            dest = str(BASE_DIR) + "/materials" + "/thumbnails"
            manager = PreviewManager(dest, create_folder=True)
            thumbnail = manager.get_jpeg_preview(
                str(BASE_DIR) + "/materials/files/" + str(file))
            return thumbnail
    for format in video_format_list:
        if str(file).endswith(format):
            options = {
                'trim': False,
                'height': 256,
                'width': 256,
                'quality': 85,
                'type': 'thumbnail'
            }
            name = str(file)[:str(file).index(format)] + ".jpg"
            dest = "/materials" + "/thumbnails/" + name
            generate_thumbnail(file, dest, options)
            return dest


def fileTypeFinder(file):
    for format in format_dict:
        if str(file).endswith(format):
            return format_dict[format]
    return "Not Known"


labels = ["Pepper__bell___Bacterial_spot", "Pepper__bell___healthy",
          "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
          "Fifth", "Tomato_Bacterial_spot", "Tomato_Late_blight", "Tomato_Leaf_Mold",
          "Tomato_Septoria_leaf_spot", "Tomato__Tomato_mosaic_virus OR Tomato_Spider_mites_Two_spotted_spider_mite",
          "Tomato__Target_Spot OR Tomato__Tomato_YellowLeaf__Curl_Virus OR Tomato_Early_blight",
          "Thirteenth", "Tomato_healthy", "Fifteenth"]


def make_predictions(path):
    image = img_utils.load_img(path, target_size=(224, 224))
    image = img_utils.img_to_array(image)
    image = image.reshape(1, 224, 224, 3)
    image = preprocess_input(image)
    model = BaseConfig.model
    prediction = model.predict(image)
    predicted = np.argmax(prediction)
    final = int(predicted)
    return labels[final]
