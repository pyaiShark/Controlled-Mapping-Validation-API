from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certification
from .serializers import CertificationSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CertificationListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active certifications",
        manual_parameters=[openapi.Parameter('course', openapi.IN_QUERY, description="Filter by course UUID", type=openapi.TYPE_STRING)] if 'course' != 'None' else [],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        certifications = Certification.active_data_objects.all()
        
        # Filtering logic
        course_id = request.query_params.get('course')
        if course_id:
            certifications = certifications.filter(course_mappings__course_id=course_id)
            
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificationRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Certification.active_data_objects.get(pk=pk)
        except Certification.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a certification",
        responses={200: CertificationSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        certification = self.get_object(pk)
        if not certification:
            return Response({"message": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        certification = self.get_object(pk)
        if not certification:
            return Response({"message": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        certification = self.get_object(pk)
        if not certification:
            return Response({"message": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a certification",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        certification = self.get_object(pk)
        if not certification:
            return Response({"message": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
            
        certification.is_active = False
        certification.save()
        return Response({"message": "Certification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
