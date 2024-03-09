import os
from typing import Tuple

from flask import (
    Flask,
    Response,
    jsonify,
    render_template,
    request,
    send_from_directory,
)
from werkzeug.utils import secure_filename

from .helpers import (
    add_media,
    add_tweet,
    delete_tweet,
    follow,
    get_tweets,
    get_user_by_word,
    like,
    unfollow,
    unlike,
)


def create_app():
    root_dir = os.path.dirname(os.path.abspath(__file__)).replace("/app", "")
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "static", "images"
    )
    static_directory = os.path.join(root_dir, "/static")
    app = Flask(
        __name__, template_folder=static_directory, static_folder=static_directory
    )
    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.errorhandler(500)
    def error_func(error) -> Tuple[Response, int]:
        return (
            jsonify(
                result=False, error_type=str(type(error)), error_message=str(error)
            ),
            500,
        )

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.route("/<path:path>")
    def send_static(path) -> Response:
        return send_from_directory(static_directory, path)

    @app.route("/api/users/me", methods=["GET"])
    def get_user() -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]
            return jsonify({"result": "true", "user": get_user_by_word(key)}), 200
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/users/<user_id>", methods=["GET"])
    def get_user_by_id(user_id: str) -> Tuple[Response, int]:
        try:
            return jsonify({"result": "true", "user": get_user_by_word(user_id)}), 200
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/users/<user_id>/follow", methods=["POST", "DELETE"])
    def follow_user_by_id(user_id) -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]

            if request.method == "POST":
                follow(user_id, key)
            elif request.method == "DELETE":
                unfollow(user_id, key)

            return jsonify({"result": "true"}), 200
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/medias", methods=["POST"])
    def init_media() -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]
            file = request.files["file"]
            if file.filename and key:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return (
                    jsonify(
                        {
                            "result": True,
                            "media_id": add_media(
                                os.path.join(app.config["UPLOAD_FOLDER"], filename)
                            ),
                        }
                    ),
                    200,
                )
            else:
                raise Exception
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/tweets", methods=["GET", "POST"])
    def get_feed() -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]

            if request.method == "GET":
                return jsonify({"result": "true", "tweets": get_tweets(key)}), 200

            data = request.json
            return jsonify({"result": "true", "tweet_id": add_tweet(key, data)}), 200
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/tweets/<tweet_id>", methods=["DELETE"])
    def delete_tweet_by_id(tweet_id) -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]

            delete_tweet(key, tweet_id)
            return jsonify({"result": "true"}), 200

        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    @app.route("/api/tweets/<tweet_id>/likes", methods=["POST", "DELETE"])
    def like_tweet(tweet_id) -> Tuple[Response, int]:
        try:
            key = request.headers["Api-key"]

            if request.method == "POST":
                like(key, tweet_id)
            else:
                unlike(key, tweet_id)
            return jsonify({"result": "true"}), 200
        except Exception as ex:
            return (
                jsonify(
                    {
                        "result": "false",
                        "error_type": str(type(ex)),
                        "error_message": str(ex),
                    }
                ),
                500,
            )

    return app
