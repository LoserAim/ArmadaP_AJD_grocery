import time

from database.models import Customer, GroceryList, GroceryItem
from faker import Faker

fake = Faker()


class FakeData:
    def __init__(self):
        self.example_customer = Customer(username=fake.name(),
                                         password=fake.password(),
                                         email=fake.email(),
                                         address=fake.address())
        self.example_grocery_list = GroceryList(
            desired_delivery=round(time.time())
        )
        self.example_grocery_item = GroceryItem(
            price_per_unit=fake.random_number(),
            quantity=fake.random_digit(),
            name=fake.first_name(),
            type=fake.last_name(),
        )
