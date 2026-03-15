import os
import sys
import django

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

def run_seed():
    print("Clearing existing data...")
    VendorProductMapping.objects.all().delete()
    ProductCourseMapping.objects.all().delete()
    CourseCertificationMapping.objects.all().delete()
    Vendor.objects.all().delete()
    Product.objects.all().delete()
    Course.objects.all().delete()
    Certification.objects.all().delete()

    print("Creating Master Entities...")
    
    # 1. Vendors
    v_aws = Vendor.objects.create(name="Amazon Web Services", code="AWS", description="Cloud computing platform")
    v_ms = Vendor.objects.create(name="Microsoft", code="MSFT", description="Technology corporation")
    v_cisco = Vendor.objects.create(name="Cisco Systems", code="CSCO", description="Networking hardware company")

    # 2. Products
    p_ec2 = Product.objects.create(name="Amazon EC2", code="EC2", description="Elastic Compute Cloud")
    p_s3 = Product.objects.create(name="Amazon S3", code="S3", description="Simple Storage Service")
    p_azure = Product.objects.create(name="Azure Virtual Machines", code="AZVM", description="Scalable compute")
    p_router = Product.objects.create(name="Cisco ISR 4000", code="ISR4K", description="Enterprise router")

    # 3. Courses
    c_aws_arch = Course.objects.create(name="AWS Solutions Architect Training", code="AWS-ARCH", description="Learn cloud architecture")
    c_aws_dev = Course.objects.create(name="AWS Developer Training", code="AWS-DEV", description="Learn cloud development")
    c_azure_admin = Course.objects.create(name="Azure Administrator Course", code="AZ-ADMIN", description="Manage Azure infrastructure")
    c_ccna_prep = Course.objects.create(name="CCNA Routing and Switching Prep", code="CCNA-PREP", description="Networking fundamentals")

    # 4. Certifications
    cert_saA = Certification.objects.create(name="AWS Certified Solutions Architect - Associate", code="SAA-C03", description="Validate cloud architecture skills")
    cert_az104 = Certification.objects.create(name="Microsoft Certified: Azure Administrator Associate", code="AZ-104", description="Azure implementation and mgmt")
    cert_ccna = Certification.objects.create(name="Cisco Certified Network Associate", code="CCNA-200-301", description="Foundation IT certification")

    print("Creating Mapping Entities...")
    
    # Vendor <-> Product Mappings
    VendorProductMapping.objects.create(vendor=v_aws, product=p_ec2, primary_mapping=True)
    VendorProductMapping.objects.create(vendor=v_aws, product=p_s3, primary_mapping=False)
    VendorProductMapping.objects.create(vendor=v_ms, product=p_azure, primary_mapping=True)
    VendorProductMapping.objects.create(vendor=v_cisco, product=p_router, primary_mapping=True)
    
    # Product <-> Course Mappings
    ProductCourseMapping.objects.create(product=p_ec2, course=c_aws_arch, primary_mapping=True)
    ProductCourseMapping.objects.create(product=p_s3, course=c_aws_arch, primary_mapping=False)
    ProductCourseMapping.objects.create(product=p_ec2, course=c_aws_dev, primary_mapping=False)
    ProductCourseMapping.objects.create(product=p_azure, course=c_azure_admin, primary_mapping=True)
    ProductCourseMapping.objects.create(product=p_router, course=c_ccna_prep, primary_mapping=True)
    
    # Course <-> Certification Mappings
    CourseCertificationMapping.objects.create(course=c_aws_arch, certification=cert_saA, primary_mapping=True)
    CourseCertificationMapping.objects.create(course=c_azure_admin, certification=cert_az104, primary_mapping=True)
    CourseCertificationMapping.objects.create(course=c_ccna_prep, certification=cert_ccna, primary_mapping=True)
    
    print("Database seeding completed successfully!")
    print(f"Total Vendors: {Vendor.objects.count()}")
    print(f"Total Products: {Product.objects.count()}")
    print(f"Total Courses: {Course.objects.count()}")
    print(f"Total Certifications: {Certification.objects.count()}")

if __name__ == '__main__':
    run_seed()
