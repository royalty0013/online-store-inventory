from django.contrib import admin
from stores.models import InventoryItem, ItemSupplier, Supplier


class ItemSupplierInline(admin.TabularInline):
    model = ItemSupplier
    extra = 1


class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone_number", "email", "address"]
    search_fields = ["name"]


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "created_at"]
    search_fields = ["name", "description"]
    inlines = [ItemSupplierInline]


class ItemSupplierAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "inventory_item",
        "supplier",
        "supply_date",
        "supplier_price",
        "quantity_supplied",
    ]
    list_filter = ["supply_date"]
    search_fields = ["inventory_item__name", "supplier__name"]


admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ItemSupplier, ItemSupplierAdmin)
