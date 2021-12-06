from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database.sql_client import db_session

db = SQLAlchemy()


def create_app(app_config):
    app = Flask(__name__)
    app.config.from_pyfile(app_config)

    db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    with app.app_context():
        from routes import views
        from rest_api.grocery_items import SingleGroceryItemAPI
        from rest_api.grocery_lists import SingleGroceryListAPI
        from rest_api.customers import SingleCustomerAPI
        app.register_blueprint(views.views_bp)
        grocery_item_api = SingleGroceryItemAPI.as_view('grocery_item')
        grocery_list_api = SingleGroceryListAPI.as_view('grocery_list')
        customer_api = SingleCustomerAPI.as_view('customer')
        app.add_url_rule(
            '/api/grocery_item/<string:item_id>',
            view_func=grocery_item_api,
            methods=['GET', 'PATCH', 'DELETE']
        )
        app.add_url_rule(
            '/api/grocery_item',
            view_func=grocery_item_api,
            methods=['POST']
        )
        app.add_url_rule(
            '/api/grocery_list/<string:item_id>',
            view_func=grocery_list_api,
            methods=['GET', 'PATCH', 'DELETE']
        )
        app.add_url_rule(
            '/api/grocery_list',
            view_func=grocery_list_api,
            methods=['POST']
        )
        app.add_url_rule(
            '/api/customer/<string:item_id>',
            view_func=customer_api,
            methods=['GET', 'PATCH', 'DELETE']
        )
        app.add_url_rule(
            '/api/customer',
            view_func=customer_api,
            methods=['POST']
        )
        return app
