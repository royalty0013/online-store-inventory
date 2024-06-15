from django.db.utils import IntegrityError
from rest_framework import serializers
from stores.models import InventoryItem, ItemSupplier, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["added_by"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["added_by"] = instance.added_by.username
        return rep


class ItemSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSupplier
        fields = "__all__"
        extra_kwargs = {"inventory_item": {"required": False}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["supplier"] = instance.supplier.name
        rep["inventory_item"] = instance.inventory_item.name
        return rep


class InventoryItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Supplier.objects.all()
    )
    item_suppliers = ItemSupplierSerializer(many=True)

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "price",
            "description",
            "created_at",
            "suppliers",
            "item_suppliers",
            "added_by",
        ]
        read_only_fields = ["added_by"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is not None:
            validated_data["added_by"] = request.user
        try:
            suppliers_data = validated_data.pop("suppliers", None)
            item_suppliers_data = validated_data.pop("item_suppliers", None)

            inventory_item_instance = InventoryItem.objects.create(**validated_data)

            for item_supplier_data in item_suppliers_data:
                supplier_instance = item_supplier_data.pop("supplier", None)
                ItemSupplier.objects.create(
                    inventory_item=inventory_item_instance,
                    supplier=supplier_instance,
                    supply_date=item_supplier_data["supply_date"],
                    supplier_price=item_supplier_data["supplier_price"],
                    quantity_supplied=item_supplier_data["quantity_supplied"],
                )
            inventory_item_instance.suppliers.set(suppliers_data)

        except IntegrityError as exception_info:
            raise serializers.ValidationError({"detail": str(exception_info)})

        return inventory_item_instance

    def update(self, instance, validated_data):
        try:
            suppliers_data = validated_data.pop("suppliers", None)
            item_suppliers_data = validated_data.pop("item_suppliers", None)

            instance.name = validated_data.get("name", instance.name)
            instance.price = validated_data.get("price", instance.price)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.save()

            if suppliers_data is not None:
                instance.suppliers.set(suppliers_data)

            if item_suppliers_data is not None:
                instance.item_suppliers.all().delete()
                for item_supplier_data in item_suppliers_data:
                    supplier_instance = item_supplier_data.pop("supplier", None)
                    ItemSupplier.objects.create(
                        inventory_item=instance,
                        supplier=supplier_instance,
                        supply_date=item_supplier_data["supply_date"],
                        supplier_price=item_supplier_data["supplier_price"],
                        quantity_supplied=item_supplier_data["quantity_supplied"],
                    )

        except IntegrityError as exception_info:
            raise serializers.ValidationError({"detail": str(exception_info)})

        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["suppliers"] = SupplierSerializer(instance.suppliers.all(), many=True).data
        rep["added_by"] = instance.added_by.username
        return rep
