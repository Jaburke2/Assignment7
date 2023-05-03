from baseapi import AbstractBookMarkAPI
from Domain import commands
from Adapters import repository

from flask import Flask, Blueprint

app = Flask(__name__)


class FlaskBookmarkAPI(AbstractBookMarkAPI):
    def __init__(self) -> None:
        super().__init__()

    def index(self) -> str:
        return commands.ListBookmarksCommand().execute()

    def one(self, id: int) -> str:
        return f"The provided id is {id}"

    def all(self) -> str:
        return "All records"

    def first(self, filter: str, value: str, sort: str) -> str:
        return "The first"

    def many(self, filter: str, value: str, sort: str) -> str:
        return "Many"

    def add(self, bookmark) -> str:
        return "Add a bookmark"

    def delete(self, bookmark) -> None:
        pass

    def update(self, bookmark) -> None:
        pass


fb = FlaskBookmarkAPI()
bp = Blueprint("flask_bookmark_api", __name__, url_prefix="/api")

bp.add_url_rule("/", "index", fb.index, methods=["GET"])
bp.add_url_rule("/one/<int:id>", "one", fb.one, methods=["GET"])
bp.add_url_rule("/all", "all", fb.all, methods=["GET"])
bp.add_url_rule("/add", "add", fb.add, methods=["POST"])
bp.add_url_rule("/delete/<int:id>", "delete", fb.delete, methods=["DELETE"])
bp.add_url_rule("/update/<int:id>", "update", fb.update, methods=["PUT"])
bp.add_url_rule(
    "/filter/<string:filter>/<string:value>/<string:sort>",
    "filter",
    fb.first,
    methods=["GET"],
)

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
