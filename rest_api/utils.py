import json

from flask import jsonify, make_response, request


def verify_and_pull_json(request):
    payload = request.json
    if not payload:
        try:
            return "success", json.loads(request.data)
        except json.JSONDecodeError as err:
            return "error", make_response(jsonify(status="error", message="JSON parse error: {}".format(err)), 406)
    return "success", payload