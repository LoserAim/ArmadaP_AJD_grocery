import pytest
from flask import url_for

from app import create_app
from database.models import Customer, GroceryItem, GroceryList
from database.sql_client import db_session
from database.sql_client import init_db
from tests.example_data import FakeData

example_data = FakeData()

@pytest.fixture(scope="module", autouse=True)
def client():
    init_db()
    app = create_app('test_config.py')
    with app.test_request_context():
        with app.app_context():
            db_session.commit()
            db_session.add(example_data.example_customer)
            db_session.add(example_data.example_grocery_list)
            db_session.add(example_data.example_grocery_item)
            db_session.commit()
            yield app.test_client()
            empty_tables = [
                Customer.__table__.delete(),
                GroceryList.__table__.delete(),
                GroceryItem.__table__.delete()]
            for table in empty_tables:
                db_session.execute(table)
            db_session.commit()


class TestCustomerAPI:
    def test_post_asserting_no_payload_results_in_406(self, client):
        request = client.post(url_for('customer'))
        assert request.status_code == 406

    def test_post_asserting_correct_payload_results_in_201(self, client):
        response = client.post(url_for('customer'), json=FakeData().example_customer.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_with_grocery_list_results_in_201(self, client):
        sample_data = FakeData()
        sample_data.example_customer.grocery_lists.append(sample_data.example_grocery_list)
        response = client.post(url_for('customer'), json=sample_data.example_customer.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_with_grocery_list_results_in_item_existing_with_child(self, client):
        sample_data = FakeData()
        sample_data.example_customer.grocery_lists.append(sample_data.example_grocery_list)
        response = client.post(url_for('customer'), json=sample_data.example_customer.as_dict())
        customer = Customer.query.filter(Customer.username == sample_data.example_customer.username).first()
        assert customer is not None and len(customer.grocery_lists) > 0
    
    def test_post_asserting_correct_payload_results_in_item_existing_in_db(self, client):
        c = FakeData().example_customer
        response = client.post(url_for('customer'), json=c.as_dict())
        customer = Customer.query.filter(Customer.username == c.username).first()
        assert customer is not None and customer.username == c.username

    def test_patch_asserting_no_payload_results_in_406(self, client):
        response = client.patch(url_for('customer', item_id=example_data.example_customer.id))
        assert response.status_code == 406

    def test_patch_asserting_no_id_results_in_405(self, client):
        c = FakeData().example_customer
        response = client.patch(url_for('customer'), json={"username": c.username})
        assert response.status_code == 405

    def test_patch_asserting_correct_payload_results_in_updated_username(self, client):
        c = FakeData().example_customer.username
        response = client.patch(url_for('customer', item_id=example_data.example_customer.id),
                                json={"username": c})

        customer = Customer.query.filter(Customer.username == c).first()
        assert customer is not None and customer.username == c

    def test_patch_asserting_correct_payload_results_in_updated_grocery_list(self, client):
        gl = FakeData().example_grocery_list
        response = client.patch(url_for('customer', item_id=example_data.example_customer.id),
                                json={"grocery_lists": [gl.as_dict()]})

        customer = Customer.query.filter(Customer.id == example_data.example_customer.id).first()
        assert customer is not None and len(customer.grocery_lists) > 0

    def test_patch_asserting_correct_payload_results_in_204(self, client):
        c = FakeData().example_customer.username
        response = client.patch(url_for('customer', item_id=example_data.example_customer.id),
                                json={"username": c})
        assert response.status_code == 204

    def test_patch_asserting_incorrect_payload_results_in_404(self, client):
        c = FakeData().example_customer.username
        response = client.patch(url_for('customer', item_id=example_data.example_customer.id),
                                json={"username2": c})
        assert response.status_code == 404

    def test_delete_asserting_incorrect_id_results_in_404(self, client):
        response = client.delete(url_for('customer', item_id=example_data.example_customer.id + '22'))
        assert response.status_code == 404

    def test_delete_asserting_no_id_results_in_405(self, client):
        response = client.delete(url_for('customer'))
        assert response.status_code == 405


class TestGroceryListAPI:
    def test_post_asserting_no_payload_results_in_406(self, client):
        request = client.post(url_for('grocery_list'))
        assert request.status_code == 406

    def test_post_asserting_correct_payload_results_in_201(self, client):
        response = client.post(url_for('grocery_list'), json=FakeData().example_grocery_list.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_with_grocery_item_results_in_201(self, client):
        sample_data = FakeData()
        sample_data.example_grocery_list.grocery_items.append(sample_data.example_grocery_item)
        response = client.post(url_for('grocery_list'), json=sample_data.example_grocery_list.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_with_grocery_item_results_in_item_existing_with_child(self, client):
        sample_data = FakeData()
        sample_data.example_grocery_list.grocery_items.append(sample_data.example_grocery_item)
        response = client.post(url_for('grocery_list'), json=sample_data.example_grocery_list.as_dict())
        id = response.json.get('data')
        if id:
            id = id.replace('Record inserted with this id: ', '')
        g_list = GroceryList.query.filter(GroceryList.id == id).first()
        assert g_list is not None and len(g_list.grocery_items) > 0

    def test_post_asserting_correct_payload_results_in_item_existing_in_db(self, client):
        g_list = FakeData().example_grocery_list
        response = client.post(url_for('grocery_list'), json=g_list.as_dict())
        grocery_list = GroceryList.query.filter(GroceryList.desired_delivery == g_list.desired_delivery).first()
        assert g_list is not None and grocery_list.desired_delivery == g_list.desired_delivery

    def test_patch_asserting_no_payload_results_in_406(self, client):
        response = client.patch(url_for('grocery_list', item_id=example_data.example_grocery_list.id))
        assert response.status_code == 406

    def test_patch_asserting_no_id_results_in_405(self, client):
        g_list = FakeData().example_grocery_list
        response = client.patch(url_for('grocery_list'), json={"desired_delivery": g_list.desired_delivery})
        assert response.status_code == 405

    def test_patch_asserting_correct_payload_results_in_updated_desired_delivery(self, client):
        g_list = FakeData().example_grocery_list.desired_delivery
        response = client.patch(url_for('grocery_list', item_id=example_data.example_grocery_list.id),
                                json={"desired_delivery": g_list})
        grocery_list = GroceryList.query.filter(GroceryList.desired_delivery == g_list).first()
        assert grocery_list is not None and grocery_list.desired_delivery == g_list

    def test_patch_asserting_correct_payload_results_in_updated_grocery_item(self, client):
        gi = FakeData().example_grocery_item
        response = client.patch(url_for('grocery_list', item_id=example_data.example_grocery_list.id),
                                json={"grocery_items": [gi.as_dict()]})

        grocery_list = GroceryList.query.filter(GroceryList.id == example_data.example_grocery_list.id).first()
        assert grocery_list is not None and len(grocery_list.grocery_items) > 0

    def test_patch_asserting_correct_payload_results_in_204(self, client):
        gl = FakeData().example_grocery_list.desired_delivery
        response = client.patch(url_for('grocery_list', item_id=example_data.example_grocery_list.id),
                                json={"desired_delivery": gl})
        assert response.status_code == 204

    def test_patch_asserting_incorrect_payload_results_in_404(self, client):
        gl = FakeData().example_grocery_list.desired_delivery
        response = client.patch(url_for('grocery_list', item_id=example_data.example_grocery_list.id),
                                json={"username2": gl })
        assert response.status_code == 404

    def test_delete_asserting_incorrect_id_results_in_404(self, client):
        response = client.delete(url_for('grocery_list', item_id=example_data.example_grocery_list.id + '22'))
        assert response.status_code == 404

    def test_delete_asserting_no_id_results_in_405(self, client):
        response = client.delete(url_for('grocery_list'))
        assert response.status_code == 405

class TestGroceryItemAPI:
    def test_post_asserting_no_payload_results_in_406(self, client):
        request = client.post(url_for('grocery_item'))
        assert request.status_code == 406

    def test_post_asserting_correct_payload_results_in_201(self, client):
        response = client.post(url_for('grocery_item'), json=FakeData().example_grocery_item.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_with_grocery_item_results_in_201(self, client):
        sample_data = FakeData()
        response = client.post(url_for('grocery_item'), json=sample_data.example_grocery_item.as_dict())
        assert response.status_code == 201

    def test_post_asserting_correct_payload_results_in_item_existing_in_db(self, client):
        g_item = FakeData().example_grocery_item
        response = client.post(url_for('grocery_item'), json=g_item.as_dict())
        grocery_item = GroceryItem.query.filter(GroceryItem.name == g_item.name).first()
        assert g_item is not None and grocery_item.name == g_item.name

    def test_patch_asserting_no_payload_results_in_406(self, client):
        response = client.patch(url_for('grocery_item', item_id=example_data.example_grocery_item.id))
        assert response.status_code == 406

    def test_patch_asserting_no_id_results_in_405(self, client):
        g_item = FakeData().example_grocery_item
        response = client.patch(url_for('grocery_item'), json={"name": g_item.name})
        assert response.status_code == 405

    def test_patch_asserting_correct_payload_results_in_updated_desired_delivery(self, client):
        g_item = FakeData().example_grocery_item.name
        response = client.patch(url_for('grocery_item', item_id=example_data.example_grocery_item.id),
                                json={"name": g_item})
        grocery_item = GroceryItem.query.filter(GroceryItem.desired_delivery == g_item).first()
        assert grocery_item is not None and grocery_item.desired_delivery == g_item

    def test_patch_asserting_correct_payload_results_in_204(self, client):
        gi = FakeData().example_grocery_item.name
        response = client.patch(url_for('grocery_item', item_id=example_data.example_grocery_item.id),
                                json={"name": gi})
        assert response.status_code == 204

    def test_patch_asserting_incorrect_payload_results_in_404(self, client):
        gi = FakeData().example_grocery_item.name
        response = client.patch(url_for('grocery_item', item_id=example_data.example_grocery_item.id),
                                json={"name2": gi})
        assert response.status_code == 404

    def test_delete_asserting_incorrect_id_results_in_404(self, client):
        response = client.delete(url_for('grocery_item', item_id=example_data.example_grocery_item.id + '22'))
        assert response.status_code == 404

    def test_delete_asserting_no_id_results_in_405(self, client):
        response = client.delete(url_for('grocery_item'))
        assert response.status_code == 405
