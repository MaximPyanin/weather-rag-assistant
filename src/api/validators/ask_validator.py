from flask import request
from werkzeug.exceptions import BadRequest
import re


class AskValidator:
    @staticmethod
    def validate():
        if not request.is_json:
            raise BadRequest("Request must be JSON")

        data = request.get_json()

        if not data:
            raise BadRequest("Request body is required")

        if "query" not in data:
            raise BadRequest("Field 'query' is required")

        query = data["query"]

        if not isinstance(query, str):
            raise BadRequest("Field 'query' must be a string")

        if not query.strip():
            raise BadRequest("Field 'query' cannot be empty")

        if len(query) > 500:
            raise BadRequest("Query too long, maximum 500 characters")

        if not re.match(r"^[a-zA-Zа-яА-Я0-9\s\.,\?!-]+$", query):
            raise BadRequest("Query contains invalid characters")

        return data
