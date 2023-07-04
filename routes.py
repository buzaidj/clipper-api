from driver import login_and_retrieve_clipper, clipper_df_to_dict
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import logging

executor = ThreadPoolExecutor(max_workers=5)
app = Flask(__name__)


@app.route("/get_clipper_usage", methods=["GET"])
def get_clipper_usage():
    try:
        with executor:
            email = request.json.get("email")
            password = request.json.get("password")

            df = login_and_retrieve_clipper(email, password)
            return jsonify(clipper_df_to_dict(df))
    except Exception as e:
        print(e)
        return f"An error occured. Please try again later. Error: {e}\n", 500


if __name__ == "__main__":
    app.run()
