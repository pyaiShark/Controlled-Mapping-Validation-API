from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CourseCertificationMappingListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active course_certification_mappings",
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = CourseCertificationMapping.active_data_objects.all()
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new course_certification_mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseCertificationMappingRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return CourseCertificationMapping.active_data_objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a course_certification_mapping",
        responses={200: CourseCertificationMappingSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a course_certification_mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a course_certification_mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a course_certification_mapping",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return Response({"message": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
            
        mapping.is_active = False
        mapping.save()
        return Response({"message": "Mapping deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
