from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CourseListOrCreateView(APIView):
    @swagger_auto_schema(
        operation_description="List all active courses",
        manual_parameters=[openapi.Parameter('product', openapi.IN_QUERY, description="Filter by product UUID", type=openapi.TYPE_STRING)] if 'product' != 'None' else [],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.active_data_objects.all()
        
        # Filtering logic
        product_id = request.query_params.get('product')
        if product_id:
            courses = courses.filter(product_mappings__product_id=product_id)
            
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseRetriveUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Course.active_data_objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a course",
        responses={200: CourseSerializer(), 404: "Not found"}
    )
    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Fully update a course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Bad Request", 404: "Not found"}
    )
    def patch(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Soft delete a course",
        responses={204: "No Content", 404: "Not found"}
    )
    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"message": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            
        course.is_active = False
        course.save()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
