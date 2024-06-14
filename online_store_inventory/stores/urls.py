from django.urls import path
from stores.views import (
    InventoryItemDetailView,
    InventoryItemListCreateView,
    SupplierDetailView,
    SupplierListCreateView,
)

app_name = "stores"


urlpatterns = [
    path(
        "inventory_items/",
        InventoryItemListCreateView.as_view(),
        name="inventory-items-list-create",
    ),
    path(
        "inventory_item/<int:pk>/",
        InventoryItemDetailView.as_view(),
        name="inventory-item-detail",
    ),
    path(
        "suppliers/",
        SupplierListCreateView.as_view(),
        name="suppliers-list-create",
    ),
    path("supplier/<int:pk>/", SupplierDetailView.as_view(), name="supplier-detail"),
]
