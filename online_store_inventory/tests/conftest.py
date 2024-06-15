import os

import django
import pytest
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.test import APIClient
from stores.models import InventoryItem, ItemSupplier, Supplier

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store_inventory.settings")
django.setup()


@pytest.fixture
def create_user_obj():
    def _create_user(username, password):
        User.objects.filter(username=username).delete()
        return User.objects.create_user(username=username, password=password)

    return _create_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, create_user_obj):
    create_user_obj("test_user", "test_pass")
    response = api_client.post(
        "/api/token/", {"username": "test_user", "password": "test_pass"}
    )
    assert response.status_code == 200
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def create_supplier_obj():
    def _create_supplier(name, phone_number, address, added_by, email=None):
        return Supplier.objects.create(
            name=name,
            phone_number=phone_number,
            address=address,
            added_by=added_by,
            email=email,
        )

    return _create_supplier


@pytest.fixture
def create_inventory_item_obj():
    def _create_inventory_item(
        name, price, description, suppliers, added_by, item_suppliers=[]
    ):
        item = InventoryItem.objects.create(
            name=name, price=price, description=description, added_by=added_by
        )

        for supplier in suppliers:
            specific_data = next(
                (item for item in item_suppliers if item["supplier"] == supplier.id),
                None,
            )
            if specific_data:
                item_suppliers.remove(specific_data)
                supplier_instance = Supplier.objects.get(
                    id=specific_data.pop("supplier")
                )
                ItemSupplier.objects.create(
                    inventory_item=item, supplier=supplier_instance, **specific_data
                )
            else:
                ItemSupplier.objects.create(
                    inventory_item=item,
                    supplier=supplier,
                    supply_date="2024-06-12",
                    supplier_price=80.00,
                    quantity_supplied=70,
                )

        return item

    return _create_inventory_item
