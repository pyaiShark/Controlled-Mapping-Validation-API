from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vendor
from .serializers import VendorSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VendorListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active vendors",
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        vendors = Vendor.active_data_objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Vendor.active_data_objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a vendor",
        responses={200: VendorSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a vendor",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
            
        # Soft delete instead of actual database deletion
        vendor.is_active = False
        vendor.save()
        return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)