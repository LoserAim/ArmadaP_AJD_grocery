import json

from flask import make_response, jsonify, request
from flask.views import MethodView

from database.models import GroceryItem, GroceryList
from database.sql_client import db_session
from rest_api.utils import verify_and_pull_json


class SingleGroceryListAPI(MethodView):
    required_fields = []
    fields = GroceryList().as_dict().keys()

    def get(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryList.query.filter(GroceryList.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was found",
                                      data=item.as_dict()), 204))

    def post(self):
        status, payload = verify_and_pull_json(request)
        if status != 'success':
            return payload
        docs = payload.pop('grocery_items')
        grocery_list = GroceryList(**payload)
        if docs:
            grocery_items = [GroceryItem(**grocery_item) for grocery_item in
                                        docs or []]
            grocery_list.grocery_items = grocery_items
        db_session.add(grocery_list)
        db_session.commit()
        return make_response(
            (jsonify(status="success", data=f"Record inserted with this id: {grocery_list.id}"), 201))

    def patch(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryList.query.filter(GroceryList.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        status, payload = verify_and_pull_json(request)
        if status != 'success':
            return payload
        contains_data_in_any_field = any([payload.get(key) for key in self.fields])
        if not contains_data_in_any_field:
            return make_response((jsonify(status="error", data=f"Payload had no data to patch requested record "
                                                               f"'{item_id}' with"), 404))
        for key in self.fields:
            if key == 'grocery_items' and payload.get(key):
                item.grocery_items.extend([GroceryItem(**grocery_item) for grocery_item in
                                           payload.get('grocery_items', []) or []])
            elif payload.get(key):
                setattr(item, key, payload.get(key))
        db_session.commit()
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was patched",
                                      data=item.as_dict()), 204))

    def delete(self, item_id=None):
        if not item_id:
            return make_response((jsonify(status="error", data=f"Missing item_id in url"), 404))
        item = GroceryList.query.filter(GroceryList.id == item_id).first()
        if not item:
            return make_response((jsonify(status="error", data=f"Record with id '{item_id}' was not found"), 404))
        item.delete()
        db_session.commit()
        return make_response((jsonify(status='success', message=f"Record with id '{item_id}' was deleted",
                                      data=item.as_dict()), 204))
