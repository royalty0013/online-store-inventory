import pytest
from django.urls import reverse
from rest_framework import status
from stores.models import InventoryItem, Supplier


@pytest.mark.django_db
def test_create_supplier(auth_client):
    url = reverse("stores:suppliers-list-create")
    data = {
        "name": "a_supplier",
        "phone_number": "0829000000",
        "email": "test@test.com",
        "address": "an_address",
    }

    response = auth_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Supplier.objects.count() == 1
    assert Supplier.objects.get().name == "a_supplier"


@pytest.mark.django_db
def test_get_suppliers(auth_client, create_supplier_obj):
    expected_response = [
        {
            "id": 1,
            "name": "test_supplier1",
            "phone_number": "0829000000",
            "email": "one@test.com",
            "address": "an_address1",
        },
        {
            "id": 2,
            "name": "test_supplier2",
            "phone_number": "0829111111",
            "email": None,
            "address": "an_address2",
        },
    ]
    create_supplier_obj(
        "test_supplier1",
        "0829000000",
        "an_address1",
        "one@test.com",
    )
    create_supplier_obj("test_supplier2", "0829111111", "an_address2")

    url = reverse("stores:suppliers-list-create")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_single_supplier(auth_client, create_supplier_obj):
    expected_response = {
        "id": 1,
        "name": "a_supplier",
        "phone_number": "0829111111",
        "email": "test@test.com",
        "address": "an_address",
    }
    supplier = create_supplier_obj(
        "a_supplier", "0829111111", "an_address", "test@test.com"
    )

    url = reverse("stores:supplier-detail", kwargs={"pk": supplier.id})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_update_supplier(auth_client, create_supplier_obj):
    supplier = create_supplier_obj("a_supplier", "0829111111", "an_address")
    assert supplier.email is None

    url = reverse("stores:supplier-detail", kwargs={"pk": supplier.id})
    data = {"email": "test@test.com"}
    response = auth_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    supplier.refresh_from_db()
    assert supplier.name == "a_supplier"
    assert supplier.email == "test@test.com"


@pytest.mark.django_db
def test_create_supplier_with_missing_fields(auth_client):
    url = reverse("stores:suppliers-list-create")
    data = {
        "phone_number": "0829000000",
        "email": "test@test.com",
        "address": "an_address",
    }

    response = auth_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field is required" in response.data["name"][0]


@pytest.mark.django_db
def test_create_supplier_with_empty_name(auth_client):
    url = reverse("stores:suppliers-list-create")
    data = {
        "name": "",
        "phone_number": "0829000000",
        "email": "test@test.com",
        "address": "an_address",
    }

    response = auth_client.post(url, data, format="json")
    print(response.data["name"][0])

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["name"][0]


@pytest.mark.django_db
def test_create_inventory_item(auth_client, create_supplier_obj):
    supplier1 = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    supplier2 = create_supplier_obj(
        "a_supply2",
        "0829111111",
        "an_address2",
        "test2@test.com",
    )

    url = reverse("stores:inventory-items-list-create")
    data = {
        "name": "an_inventory_item",
        "price": "245.35",
        "description": "An inventory item",
        "suppliers": [supplier1.id, supplier2.id],
        "item_suppliers": [
            {
                "supplier": supplier1.id,
                "supply_date": "2024-06-01",
                "supplier_price": "110.00",
                "quantity_supplied": 70,
            },
            {
                "supplier": supplier2.id,
                "supply_date": "2024-06-02",
                "supplier_price": "120.00",
                "quantity_supplied": 40,
            },
        ],
    }
    response = auth_client.post(url, data, format="json")

    expected_response_data = {
        "id": response.data["id"],
        "name": "an_inventory_item",
        "price": "245.35",
        "description": "An inventory item",
        "created_at": response.data["created_at"],
        "suppliers": [
            {
                "id": supplier1.id,
                "name": supplier1.name,
                "phone_number": supplier1.phone_number,
                "email": supplier1.email,
                "address": supplier1.address,
            },
            {
                "id": supplier2.id,
                "name": supplier2.name,
                "phone_number": supplier2.phone_number,
                "email": supplier2.email,
                "address": supplier2.address,
            },
        ],
        "item_suppliers": [
            {
                "id": response.data["item_suppliers"][0]["id"],
                "inventory_item": response.data["name"],
                "supplier": supplier1.name,
                "supply_date": "2024-06-01",
                "supplier_price": "110.00",
                "quantity_supplied": 70,
            },
            {
                "id": response.data["item_suppliers"][1]["id"],
                "inventory_item": response.data["name"],
                "supplier": supplier2.name,
                "supply_date": "2024-06-02",
                "supplier_price": "120.00",
                "quantity_supplied": 40,
            },
        ],
    }
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response_data
    assert InventoryItem.objects.count() == 1


@pytest.mark.django_db
def test_get_inventory_items(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier1 = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    supplier2 = create_supplier_obj(
        "a_supply2",
        "0829111111",
        "an_address2",
        "test2@test.com",
    )

    create_inventory_item_obj(
        "an_inventory_item", 140.00, "a_description", [supplier1, supplier2]
    )
    create_inventory_item_obj(
        "an_inventory_item1", 110.00, "a_description2", [supplier2]
    )

    url = reverse("stores:inventory-items-list-create")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "an_inventory_item"
    assert response.data[1]["name"] == "an_inventory_item1"


@pytest.mark.django_db
def test_get_single_inventory_item(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    item = create_inventory_item_obj(
        "an_inventory_item", 140.00, "a_description", [supplier]
    )

    url = reverse("stores:inventory-item-detail", kwargs={"pk": item.id})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "an_inventory_item"


@pytest.mark.django_db
def test_update_inventory_item(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    item = create_inventory_item_obj(
        "an_inventory_item", 140.00, "a_description", [supplier]
    )

    url = reverse("stores:inventory-item-detail", kwargs={"pk": item.id})
    data = {"name": "a_supply_item", "price": 145.00}
    response = auth_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    item.refresh_from_db()
    assert item.name == "a_supply_item"
    assert item.price == 145.00


@pytest.mark.django_db
def test_partial_update_inventory_item(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    item = create_inventory_item_obj(
        "an_inventory_item", 140.00, "a_description", [supplier]
    )

    url = reverse("stores:inventory-item-detail", kwargs={"pk": item.id})
    data = {"price": "150.00"}
    response = auth_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    item.refresh_from_db()
    assert item.price == 150.00


@pytest.mark.django_db
def test_delete_inventory_item(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier = create_supplier_obj(
        "a_supply1",
        "082900000",
        "an_address",
        "test@test.com",
    )
    item = create_inventory_item_obj(
        "an_inventory_item", 140.00, "a_description", [supplier]
    )

    url = reverse("stores:inventory-item-detail", kwargs={"pk": item.id})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert InventoryItem.objects.count() == 0


@pytest.mark.django_db
def test_create_inventory_item_with_duplicate_name(
    auth_client, create_supplier_obj, create_inventory_item_obj
):
    supplier1 = create_supplier_obj(
        "Supplier One", "1234567890", "supplier1@example.com", "Address One"
    )
    create_inventory_item_obj("Item One", "50.00", "Description One", [supplier1])

    url = reverse("stores:inventory-items-list-create")
    data = {
        "name": "Item One",
        "price": 140.00,
        "description": "A duplicate inventory item",
        "suppliers": [supplier1.id],
    }
    response = auth_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["name"][0] == "inventory item with this name already exists."


@pytest.mark.django_db
def test_create_inventory_item_with_missing_fields(auth_client):
    url = reverse("stores:inventory-items-list-create")
    data = {"price": 50.20, "description": "an_inventory_item"}

    response = auth_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field is required" in response.data["name"][0]


@pytest.mark.django_db
def test_create_inventory_item_with_invalid_supplier(auth_client):
    url = reverse("stores:inventory-items-list-create")
    data = {
        "name": "Invalid Supplier Item",
        "price": 140.00,
        "description": "A new inventory item",
        "suppliers": [50],
        "item_suppliers": [
            {
                "supplier": 999,
                "supply_date": "2024-06-01",
                "supplier_price": "110.00",
                "quantity_supplied": 50,
            }
        ],
    }
    response = auth_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "object does not exist" in response.data["suppliers"][0]
