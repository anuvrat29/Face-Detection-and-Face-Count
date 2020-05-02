"""
    This code will take care of surveillance.
"""
# pylint: disable=E1101
# pylint: disable=E0211
# pylint: disable=W0702
import os
import glob
import base64
from flask import Flask, render_template, request, send_file, jsonify

from utilities.detect_person import Person
from utilities.config import SNAPPED_IMAGE, PREDICTED_IMAGE

APP = Flask(__name__, template_folder="frontend")

class Surveillance:
    """
        This class contains all the methods of surveillance.
    """
    @staticmethod
    @APP.route("/")
    def index():
        """
            Index page which will be hit when you open base URL.
        """
        return render_template("index.html")

    @staticmethod
    @APP.after_request
    def add_header(response):
        """
            Add response headers.
        """
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @staticmethod
    @APP.route("/submit/<imagename>", methods=["GET"])
    def download_image(imagename):
        """
            Get image and detect face.
        """
        return send_file(os.path.join(PREDICTED_IMAGE, imagename),\
                            as_attachment=False, cache_timeout=0)

    @classmethod
    def save_image(cls, image_object, filename):
        """
            This method will save the image.
        """
        if not os.path.isdir(SNAPPED_IMAGE):
            os.mkdir(SNAPPED_IMAGE)
        else:
            for image in glob.glob(os.path.join(SNAPPED_IMAGE, "*.*")):
                try:
                    os.remove(image)
                except:
                    pass

        filepath = os.path.join(SNAPPED_IMAGE, f"{filename}.jpg")
        with open(filepath, "wb") as file:
            file.write(base64.b64decode(str.encode(image_object, encoding="ascii")))
        return filepath

    @staticmethod
    @APP.route("/submit", methods=["POST"])
    def get_image():
        """
            Get image and detect face.
        """
        filepath = Surveillance().save_image(request.json["file"], request.json["filename"])
        return jsonify(Person().detect_person(filepath))

if __name__ == '__main__':
    APP.config["CACHE_TYPE"] = "null"
    APP.jinja_env.cache = {}
    APP.run(host="127.0.0.1", port=65000, debug=True)
