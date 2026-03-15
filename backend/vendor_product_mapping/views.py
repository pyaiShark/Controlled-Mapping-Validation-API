from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class VendorProductMappingListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active vendor_product_mappings",
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = VendorProductMapping.active_data_objects.all()
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new vendor_product_mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorProductMappingRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return VendorProductMapping.active_data_objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a vendor_product_mapping",
        responses={200: VendorProductMappingSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a vendor_product_mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a vendor_product_mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a vendor_product_mapping",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        mapping.is_active = False
        mapping.save()
        return Response({"message": "Mapping deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
