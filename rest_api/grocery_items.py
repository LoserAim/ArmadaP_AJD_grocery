import json

from flask import make_response, jsonify, request
from flask.views import MethodView

from database.models import GroceryItem
from database.sql_client import db_session
from rest_api.utils import verify_and_pull_json


class SingleGroceryItemAPI(MethodView):
    required_fields = ['username', 'password']

    def get(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryItem.query.filter(GroceryItem.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was found",
                                      data=item.as_dict()), 204))

    def post(self):
        status, payload = verify_and_pull_json(request)
        if status != 'success':
            return payload
        contains_required_fields = any([payload.get(key) for key in self.required_fields])
        if not contains_required_fields:
            return make_response((jsonify(status="error", data=f"Payload was missing one or more required fields: "
                                                               f"{', '.join(self.required_fields)}"), 404))
        grocery_item = GroceryItem(**payload)
        db_session.add(grocery_item)
        db_session.commit()
        return make_response(
            (jsonify(status="success", data=f"Record Inserted with this id: {grocery_item.id}"), 201))

    def patch(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryItem.query.filter(GroceryItem.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        status, payload = verify_and_pull_json(request)
        if status != 'success':
            return payload
        contains_data_in_any_field = any([payload.get(key) for key in GroceryItem().as_dict().keys()])
        if not contains_data_in_any_field:
            return make_response((jsonify(status="error", data=f"Payload had no data to patch requested record "
                                                               f"'{item_id}' with"), 404))
        for key in GroceryItem().as_dict().keys():
            if payload.get(key):
                setattr(item, key, payload.get(key))
        db_session.commit()
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was patched",
                                      data=item.as_dict()), 204))

    def delete(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryItem.query.filter(GroceryItem.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        item.delete()
        db_session.commit()
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was deleted",
                                      data=item.as_dict()), 204))
