import pytest
from flask import url_for

from app import create_app
from database.models import Customer, GroceryItem, GroceryList
from database.sql_client import db_session
from database.sql_client import init_db

example_customer = Customer(
            username="SavinGanes",
            password="password",
            email="savin.ganes@test.com",
            address="1233 SW test drive, CityTest, StateTest, 11001")
        


@pytest.fixture(autouse=True)
def client():
    init_db()
    app = create_app('test_config.py')
    with app.test_request_context():
        with app.app_context():
            db_session.commit()
            c = Customer(username="GelsingPat",
                         password="password",
                         email="pat.gelsing@test.com",
                         address="1234 SW test drive, CityTest, StateTest, 11001")
            db_session.add(c)
            db_session.commit()
            yield app.test_client(), c
            empty_tables = [
                Customer.__table__.delete(),
                GroceryList.__table__.delete(),
                GroceryItem.__table__.delete()]
            for table in empty_tables:
                db_session.execute(table)
            db_session.commit()


class TestCustomerAPI:
    def test_post_asserting_no_payload_results_in_406(self, client):
        request = client[0].post(url_for('customer'))
        assert request.status_code == 406

    def test_post_asserting_correct_payload_results_in_201(self, client):
        request = client[0].post(url_for('customer'), json=example_customer.as_dict())
        assert request.status_code == 201
    
    def test_post_asserting_correct_payload_results_in_item_existing_in_db(self, client):
        request = client[0].post(url_for('customer'), json=example_customer.as_dict())
        customer = Customer.query.filter(Customer.username == example_customer.username).first()
        assert customer is not None and customer.username == example_customer.username

    def test_patch_asserting_no_payload_results_in_406(self, client):
        request = client[0].patch(url_for('customer', item_id=client[1].id))
        assert request.status_code == 406
