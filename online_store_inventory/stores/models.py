from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="currency in euro(€)"
    )
    description = models.TextField()
    suppliers = models.ManyToManyField(
        Supplier, through="ItemSupplier", related_name="items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ItemSupplier(models.Model):
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name="item_suppliers"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="inventory_items"
    )
    supply_date = models.DateField()
    supplier_price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="currency in euro(€)"
    )
    quantity_supplied = models.IntegerField()

    def __str__(self):
        return f"{self.inventory_item.name} - {self.supplier.name}"
