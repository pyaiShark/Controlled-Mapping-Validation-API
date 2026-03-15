from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProductListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active products",
        manual_parameters=[openapi.Parameter('vendor', openapi.IN_QUERY, description="Filter by vendor UUID", type=openapi.TYPE_STRING)] if 'vendor' != 'None' else [],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        products = Product.active_data_objects.all()
        
        # Filtering logic
        vendor_id = request.query_params.get('vendor')
        if vendor_id:
            products = products.filter(vendor_mappings__vendor_id=vendor_id)
            
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Product.active_data_objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a product",
        responses={200: ProductSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a product",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        product.is_active = False
        product.save()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
