from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from stores.models import InventoryItem, Supplier
from stores.serializers import InventoryItemSerializer, SupplierSerializer


class SupplierListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SupplierSerializer

    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = self.serializer_class(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SupplierSerializer

    def get_object(self, pk):
        return get_object_or_404(Supplier, pk=pk)

    def get(self, request, pk):
        supplier = self.get_object(pk)
        serializer = self.serializer_class(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        supplier = self.get_object(pk)
        serializer = self.serializer_class(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryItemSerializer

    def get(self, request):
        items = InventoryItem.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                serializer.save(added_by=request.user)
            except ValidationError as exception_info:
                return Response(
                    {"error": str(exception_info)}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryItemSerializer

    def get_object(self, pk):
        return get_object_or_404(InventoryItem, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(
            item, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as exception_info:
                return Response(
                    {"error": str(exception_info)}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
